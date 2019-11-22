from flask import Blueprint, jsonify, request, render_template

import json
import requests

from PicMetric.classes.img_handler import Img_Handler
from PicMetric.models.resnet50 import resnet
from PicMetric.models.yolov3 import yolov3
from PicMetric.models.faces import faces
from PIL import Image
import os
import io

demo_url_bp = Blueprint('demo_url_bp', __name__)


@demo_url_bp.route('/demo_url', methods=['GET', 'POST'])
def demo_url():
    """endpoint for image urls

    set model list (hardcoded currently)
    set name for file to store locally
    get url from html form
    get iamge from url
    save with pillow
    open as readable file like object
    pass to img_handler for processing
    remove local file on completion
    
    Returns:
        [json response] -- [contains the data from running models on the image]
    """
    model_list = [resnet, yolov3, faces]
    filename = 'PicMetric/assets/infile.png'
    url = request.form.get('url')
    raw = requests.get(url).content

    with open(filename, 'wb') as out_file:
        Image.open(io.BytesIO(raw)).save(out_file, format='png')
    with open(filename, 'rb') as in_file:
        data = Img_Handler(in_file, model_list).get_pred_data()
    os.remove(filename)

    return render_template('results.html', **data)

