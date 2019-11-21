import os
import io
import requests
from PIL import Image
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from imageai.Detection import ObjectDetection
from PicMetric.functions.s3_funcs import upload_file_to_s3, S3_BUCKET, s3, S3_LOCATION

weights_url = 'https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5'
weights_path = "PicMetric/assets/weights/yolo.h5"
temp_output_path = os.path.join('PicMetric/assets/temp', "temp.jpg")



def yolov3(input_path):
    if not os.path.exists(weights_path):
        try:
            with requests.get(weights_url) as weights, open(temp_output_path, 'wb') as outfile:
                outfile.write(weights.content)
        except:
            return 'error'

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(weights_path)
    detector.loadModel()
    detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=temp_output_path)

    data = dict()
    filename= os.path.join(os.path.splitext(input_path)[0], '_yolov3.jgp')
    data['url'] = "{}{}".format(S3_LOCATION, filename)
    s3.upload_file(temp_output_path, S3_BUCKET, filename)
    
    for eachItem in detection:
        data[eachItem["name"]] = str(eachItem["percentage_probability"])

    return data
