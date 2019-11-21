import os
import requests
import hashlib
from decouple import config
from imageai.Detection import ObjectDetection
from PicMetric.classes.img_handler import upload_file_to_s3

weights_url = 'https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5'
weights_path = "PicMetric/assets/weights/yolo.h5"
temp_output_path = os.path.join('PicMetric/assets/temp', "temp.png")

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
    with open(temp_output_path, 'rb') as outfile, open(input_path, 'rb') as infile:
        filename= hashlib.md5(infile.read()).hexdigest() + '_yolov3.png'
        data['url'] = upload_file_to_s3(outfile, config('S3_BUCKET'), filename)
    
    for item in detection:
        data[item["name"]] = str(item["percentage_probability"])

    return data
