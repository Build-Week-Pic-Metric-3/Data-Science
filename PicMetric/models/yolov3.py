import os
import io
import requests
from PIL import Image
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from imageai.Detection import ObjectDetection

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

    img_io = io.StringIO()
    Image.open(temp_output_path)
    img_io.seek(0)
    
    data={'img': str(img_io)}
    for eachItem in detection:
        data[eachItem["name"]] = str(eachItem["percentage_probability"])

    return data
