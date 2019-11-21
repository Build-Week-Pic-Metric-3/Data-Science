import io
import os
import hashlib
import requests
import json
from decouple import config

from PIL import Image
from PicMetric.schema import DB, HashTable
from PicMetric.functions.s3_funcs import upload_file_to_s3, S3_BUCKET


IMGDIR_PATH = 'PicMetric/assets/temp'
UPLOAD_FOLDER = 'PicMetric/assets/temp/'

class Img_Handler:
    def __init__(self, img_file, model_list):
        self.model_list = model_list
        self.img_url = upload_file_to_s3(img_file, S3_BUCKET)
        self.img_file = requests.get(self.img_url).content


    def get_pred_data(self):
        data = {'original': self.img_url}
        data['hash'] = hashlib.md5(self.img_file).hexdigest()

        is_img_dup = HashTable.query.filter(HashTable.hash == data['hash']).all()
        if is_img_dup:
            for model in self.model_list:
                data[model.__name__] = getattr(is_img_dup[0], model.__name__)
            data['hash'] = is_img_dup[0].hash
            data['source'] = is_img_dup[0].source
            data['original'] = is_img_dup[0].original
            data['error'] = ""
            return data
        
        output_filename = os.path.join(IMGDIR_PATH, f"{data['hash']}.png")

        with open(output_filename, 'wb') as out_file:
            Image.open(io.BytesIO(self.img_file)).save(out_file, format='png')

        for model in self.model_list:
            data[model.__name__] = model(output_filename)

            if 'url' in data[model.__name__]:
                data['source'] = data[model.__name__]['url']
                del data[model.__name__]['url']
            data[model.__name__] = json.dumps(data[model.__name__])

        db_entry = HashTable(**data)
        DB.session.add(db_entry)
        DB.session.commit()

        for filename in os.listdir(IMGDIR_PATH):
            os.remove(os.path.join(IMGDIR_PATH, filename))
        
        with open(os.path.join(IMGDIR_PATH, 'placeholder.py'), 'wb'):
            data['error'] = ""

        return data