from flask import Blueprint, request
from PicMetric.classes.img_handler import Img_Handler

bis_bp = Blueprint('bis_bp', __name__)

@bis_bp.route('/batch_img_summary')
def batch_img_summary():
    urls = ['test_url', 'test_url2', 'test_url3']
    data = Img_Handler(urls).get_data()

    return data