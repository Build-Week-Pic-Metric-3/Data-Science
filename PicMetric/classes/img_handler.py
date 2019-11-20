import io
import os
import hashlib
import requests
import json

from PIL import Image
from PicMetric.schema import DB, HashTable

IMGDIR_PATH = 'PicMetric/assets/temp'

class Img_Handler:
    def __init__(self, url_list, model_list):
        self.url_list = url_list
        self.model_list = model_list
    
    def get_data(self):
        data = []
        for url in self.url_list:
            data.append(self.get_pred_data(url))
        return data

    def get_pred_data(self, url):
        data = {'source': url}

        is_url_dup = HashTable.query.filter(HashTable.source == url).all()
        if is_url_dup:
            for model in self.model_list:
                data[model.__name__] = getattr(is_url_dup[0], model.__name__)
            data['hash'] = is_url_dup[0].hash
            data['error'] = ""
            return data

        try:
            with requests.get(url) as response:
                content = response.content
                raw = io.BytesIO(response.content)

        except:
            data['error'] = 'url_error'

            return data
        
        else:
            data['hash'] = hashlib.md5(content).hexdigest()
            is_img_dup = HashTable.query.filter(HashTable.hash == data['hash']).all()
            if is_img_dup:
                for model in self.model_list:
                    data[model.__name__] = getattr(is_img_dup[0], model.__name__)
                data['hash'] = is_img_dup[0].hash
                data['error'] = ""
                return data
            
            output_filename = os.path.join(IMGDIR_PATH, f"{data['hash']}.png")
            img = Image.open(raw)

            with open(output_filename, 'wb') as out_file:
                img.save(out_file, format='png')

            for model in self.model_list:
                data[model.__name__] = model(output_filename)
                imgs = dict()
                if 'img' in data[model.__name__]:
                    imgs[model.__name__] = data[model.__name__]['img']
                    del data[model.__name__]['img']
                data[model.__name__] = json.dumps(data[model.__name__])

            db_entry = HashTable(**data)
            DB.session.add(db_entry)
            DB.session.commit()

            if imgs:
                for key, value in imgs.items():
                    data[key] = json.loads(data[key])
                    data[key]['img'] = value

            for filename in os.listdir(IMGDIR_PATH):
                os.remove(os.path.join(IMGDIR_PATH, filename))

            data['error'] = ""

            return data