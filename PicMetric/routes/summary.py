import json

from flask import Blueprint

from PicMetric.classes.img_handler import Img_Handler

sum_bp = Blueprint('sum_bp', __name__)

@sum_bp.route('/summary')
def summary():
    url = 'https://i.redd.it/xo6qisuwsbs31.jpg'
    data = Img_Handler([url]).get_data()

    return data