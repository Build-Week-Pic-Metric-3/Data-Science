import io
import os
import hashlib
import requests

from PIL import Image
from PicMetric.schema import DB, HashTable

IMGDIR_PATH = 'PicMetric/assets'

class Img_Handler:
    def __init__(self, url_list):
        self.url_list = url_list
    
    def get_data(self, model_func):
        data = dict()
        for url in self.url_list:
            data[url] = get_pred_data(url, model_func)
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
                data[model.__name__] = str(model(output_filename))

            db_entry = HashTable(**data)
            DB.session.add(db_entry)
            DB.session.commit()

            os.remove(output_filename)
            data['error'] = ""

        