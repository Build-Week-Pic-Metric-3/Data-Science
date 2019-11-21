from flask import Blueprint, jsonify, request

import json

from PicMetric.classes.img_handler import Img_Handler
from PicMetric.models.resnet50 import resnet
from PicMetric.models.yolov3 import yolov3

do_data_science_bp = Blueprint('do_data_science_bp', __name__)


@do_data_science_bp.route('/do_data_science', methods=['GET', 'POST'])
def do_data_science():
    model_list = [resnet, yolov3]
    data = Img_Handler(request.files['file'], model_list).get_pred_data()
    
    return jsonify(data)