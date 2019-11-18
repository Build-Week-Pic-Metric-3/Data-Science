from flask import Blueprint, jsonify

import json

from PicMetric.classes.img_handler import Img_Handler
from PicMetric.models.resnet50 import resnet

do_data_science_bp = Blueprint('do_data_science_bp', __name__)

@do_data_science_bp.route('/do_data_science', methods=['GET', 'POST'])
def do_data_science():
    url_list = [
        'https://i.redd.it/t5gqutndubs31.png',
        'https://i.redd.it/wutifutmubs31.jpg',
        'https://i.redd.it/5q7spoypubs31.jpg',
        'https://i.redd.it/a2koy4ptubs31.jpg',
        'https://i.redd.it/pk77o0u4vbs31.jpg'
    ]
    model_list = [resnet]

    data = Img_Handler(url_list, model_list).get_data()

    return jsonify(data)