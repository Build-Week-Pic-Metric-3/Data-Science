import io
import os
import hashlib
import requests
import json

from PIL import Image
from PIL.ImageOps import fit

from PicMetric.models import DB, HashTable
IMGDIR_PATH = 'PicMetric/assets/imgdir'

def get_pred_data(url, func):
    data = dict()
    is_url_dup = HashTable.query.filter(HashTable.url == url).all()
    if not is_url_dup:
        try:
            with requests.get(url) as response:
                content = response.content
                raw = io.BytesIO(response.content)

            filehash = hashlib.md5(content).hexdigest()
            data['hash'] = filehash
            output_filename = os.path.join(IMGDIR_PATH, f"{filehash}.png")

            
            with open(output_filename, 'wb') as out_file:
                img = Image.open(raw)
                img.save(out_file, format='png')

            is_img_dup = HashTable.query.filter(HashTable.hash == filehash).all()
            if is_img_dup:
                data['pred'] = is_img_dup[0].pred
                data['hash'] = is_img_dup[0].hash

            else:
                data['pred'] = str(func(output_filename))

                db_entry = HashTable(hash=filehash, pred=data['pred'], url=url)
                DB.session.add(db_entry)
                DB.session.commit()
            
            os.remove(output_filename)
            return json.dumps(data)
        except Exception as e:
            data['pred'] = 'error'
            data['hash'] = 'error'
            data['e'] = str(e)

            db_entry = HashTable(hash=data['hash'], pred=data['pred'], url=url)
            DB.session.add(db_entry)
            DB.session.commit()

            return json.dumps(data)
    else:
        data['pred'] = is_url_dup[0].pred
        data['hash'] = is_url_dup[0].hash
        return json.dumps(data)