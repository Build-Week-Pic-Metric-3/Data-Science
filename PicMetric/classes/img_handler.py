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

#Declaring Variables for image handling
IMGDIR_PATH = 'PicMetric/assets/temp'
UPLOAD_FOLDER = 'PicMetric/assets/temp/'
ExtraArgs = json.loads(config('ExtraArgs'))

#aws variables declared in .env
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
        #models that will be run on the images
        self.model_list = model_list
        self.img_file = img_file
        self.hash = hashlib.md5(img_file.read()).hexdigest()
        #moves the cursor back to the begginign of the file to do another read call
        self.img_file.seek(0)
        #original URL is hash of the image to s3
        self.img_url = upload_file_to_s3(self.img_file, config('S3_BUCKET'), self.hash+'.png')
        #pulls file back down from s3
        self.img_file = requests.get(self.img_url).content

    def get_pred_data(self):
        #data object as a dictionary of URL of the image and a hash of the image
        data = {'original': self.img_url, 'hash': self.hash}
        
        #checking to see if the image uploaded shares a hash within the database.
        is_img_dup = HashTable.query.filter(HashTable.hash == data['hash']).all()
        #if there is a duplicated hash of the image it runs logic to pull into a DB response
        if is_img_dup:
            for model in self.model_list:
                if model.__name__ != 'faces':
                    data[model.__name__] = getattr(is_img_dup[0], model.__name__)
            data['hash'] = is_img_dup[0].hash
            data['source'] = is_img_dup[0].source
            data['original'] = is_img_dup[0].original
            data['error'] = ""
            return data
        
        #gets the filepath to the hashed image locally
        output_filename = os.path.join(IMGDIR_PATH, f"{data['hash']}.png")
        
        #loads the file from s3 as a .png
        with open(output_filename, 'wb') as out_file:
            Image.open(io.BytesIO(requests.get(self.img_url).content)).save(out_file, format='png')

        #loads the model and runs it on the original picture loaded from s3    
        for model in self.model_list:
            data[model.__name__] = model(output_filename)

            #building out the object to put in the response and database
            if 'url' in data[model.__name__]:
                data[model.__name__+'_source'] = data[model.__name__]['url']
                del data[model.__name__]['url']
            if data[model.__name__]: data[model.__name__] = json.dumps(data[model.__name__])
            else: del data[model.__name__]

        #writes analysis to database     
        DB.session.add(HashTable(**data))
        DB.session.commit()

        #cleans up the file in temp directory
        for filename in os.listdir(IMGDIR_PATH):
            os.remove(os.path.join(IMGDIR_PATH, filename))
        
        #creates a placeholder file to preserve the heirarchy
        #get to the end of the file, so errors is nothing so write it as such
        with open(os.path.join(IMGDIR_PATH, 'placeholder.py'), 'wb'):
            data['error'] = ""

        return data