import io
import os
import hashlib
import requests

from PIL import Image

IMGDIR_PATH = 'PicMetric/assets'

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
        try:
            with requests.get(url) as response:
                content = response.content
                raw = io.BytesIO(response.content)

        except:
            data['error'] = 'url_error'

            return data
        
        else:
            data['hash'] = hashlib.md5(content).hexdigest()
            output_filename = os.path.join(IMGDIR_PATH, f"{data['hash']}.png")
            img = Image.open(raw)

            with open(output_filename, 'wb') as out_file:
                img.save(out_file, format='png')

            for model in self.model_list:
                data[model.__name__] = str(model(output_filename))

            os.remove(output_filename)
            data['error'] = ""

            return data
        