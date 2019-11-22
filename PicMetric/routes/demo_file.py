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

demo_file_bp = Blueprint('demo_file_bp', __name__)


@demo_file_bp.route('/demo_file', methods=['GET', 'POST'])
def demo_file():
    """endpoint for files

    set model list (hardcoded right now)
    pull file from form
    
    Returns:
        [json response] -- [contains the data from running models on the image]
    """
    model_list = [resnet, yolov3, faces]
    infile = request.files['file']
    data = Img_Handler(infile, model_list).get_pred_data()

    return render_template('results.html', **data)
