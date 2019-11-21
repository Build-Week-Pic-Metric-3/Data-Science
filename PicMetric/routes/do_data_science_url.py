from flask import Blueprint, jsonify, request

import json
import requests

from PicMetric.classes.img_handler import Img_Handler
from PicMetric.models.resnet50 import resnet
from PicMetric.models.yolov3 import yolov3
from PicMetric.models.faces import faces
from PIL import Image
import os
import io

do_data_science_url_bp = Blueprint('do_data_science_url_bp', __name__)


@do_data_science_url_bp.route('/do_data_science_url', methods=['GET', 'POST'])
def do_data_science_url():
    model_list = [resnet, yolov3, faces]

    filename = 'PicMetric/assets/infile.png'

    #parses url from the post request
    url = request.form.get('url')
    raw = requests.get(url).content
    #writes it to a .png locally, then runs analysis against it across the models
    with open(filename, 'wb') as out_file:
        Image.open(io.BytesIO(raw)).save(out_file, format='png')
    with open(filename, 'rb') as in_file:
        data = Img_Handler(in_file, model_list).get_pred_data()
    os.remove(filename)
    return jsonify(data)

