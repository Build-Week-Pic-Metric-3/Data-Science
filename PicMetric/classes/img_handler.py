import io
import os
import hashlib
import requests
import json
from decouple import config
from werkzeug.utils import secure_filename
import boto3, botocore

from PIL import Image
from PicMetric.schema import DB, HashTable
from shutil import copystat


IMGDIR_PATH = 'PicMetric/assets/temp'
UPLOAD_FOLDER = 'PicMetric/assets/temp/'
ExtraArgs = json.loads(config('ExtraArgs'))

AWS = {
    'aws_access_key_id': config('S3_KEY'),
    'aws_secret_access_key': config('S3_SECRET')
}
s3 = boto3.client("s3", **AWS)

def upload_file_to_s3(*args):
    try: s3.upload_fileobj(*args, ExtraArgs=ExtraArgs)
    except Exception as e: return str(e)
    return "{}{}".format(config('S3_LOCATION'), args[2])

class Img_Handler:
    def __init__(self, img_file, model_list):
        self.model_list = model_list
        self.img_file = img_file
        self.hash = hashlib.md5(img_file.read()).hexdigest()
        self.img_file.seek(0)
        self.img_url = upload_file_to_s3(self.img_file, config('S3_BUCKET'), self.hash+'.png')
        self.img_file = requests.get(self.img_url).content

    def get_pred_data(self):
        data = {'original': self.img_url, 'hash': self.hash}

        is_img_dup = HashTable.query.filter(HashTable.hash == data['hash']).all()
        if is_img_dup:
            for model in self.model_list:
                if model.__name__ != 'faces':
                    data[model.__name__] = getattr(is_img_dup[0], model.__name__)
            data['hash'] = is_img_dup[0].hash
            data['faces_source'] = is_img_dup[0].faces_source
            data['yolov3_source'] = is_img_dup[0].yolov3_source
            data['original'] = is_img_dup[0].original
            data['error'] = ""
            return data
        
        output_filename = os.path.join(IMGDIR_PATH, f"{data['hash']}.png")

        with open(output_filename, 'wb') as out_file:
            Image.open(io.BytesIO(requests.get(self.img_url).content)).save(out_file, format='png')

        for model in self.model_list:
            data[model.__name__] = model(output_filename)

            if 'url' in data[model.__name__]:
                data[model.__name__+'_source'] = data[model.__name__]['url']
                del data[model.__name__]['url']
            if data[model.__name__]: data[model.__name__] = json.dumps(data[model.__name__])
            else: del data[model.__name__]

        DB.session.add(HashTable(**data))
        DB.session.commit()

        for filename in os.listdir(IMGDIR_PATH):
            os.remove(os.path.join(IMGDIR_PATH, filename))
        
        with open(os.path.join(IMGDIR_PATH, 'placeholder.py'), 'wb'):
            data['error'] = ""

        return data