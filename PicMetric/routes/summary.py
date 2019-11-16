import json

from flask import Blueprint

from PicMetric.classes.imgdir_handler import Imgdir_Handler

sum_bp = Blueprint('sum_bp', __name__)

@sum_bp.route('/summary')
def summary():
    img_url = 'test_url'
    data = Imgdir_Handler([img_url]).get_data()

    return data