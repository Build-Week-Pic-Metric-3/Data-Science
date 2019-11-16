import io
import os
import hashlib
import requests
import json

from PIL import Image
from PIL.ImageOps import fit

from PicMetric.models import DB, HashTable

def get_pred_data(url):
    data = dict()
    is_url_dup = HashTable.query.filter(HashTable.url == url).all()
    if not is_url_dup:
        try:
            with requests.get(url) as response:
                raw = io.BytesIO(response.content)

            filehash = hashlib.md5(raw).hexdigest()
            data['hash'] = filehash

            is_img_dup = HashTable.query.filter(HashTable.hash == filehash).all()
            if is_img_dup:
                data['pred'] = is_not_img_dup

            else:
                img = Image.open(raw)

                data['pred'] = 'do prediction'

                db_entry = HashTable(hash=filehash, pred=pred, url=url)
                DB.session.add(db_entry)
                DB.session.commit()
            
            return data
        except Exception as e:
            data['pred'] = 'error'
            data['hash'] = 'error'

            db_entry = HashTable(hash=data['hash'], pred=data['pred'], url=url)
            DB.session.add(db_entry)
            DB.session.commit()

            return json.dumps(data)
    else:
        data['pred'] = is_not_url_dup
        return json.dumps(data)