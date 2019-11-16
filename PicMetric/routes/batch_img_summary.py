from flask import Blueprint, request
from PicMetric.classes.imgdir_handler import Imgdir_Handler

bis_bp = Blueprint('bis_bp', __name__)

@bis_bp.route('/batch_img_summary')
def batch_img_summary():
    img_urls = ['test_url', 'test_url2', 'test_url3']
    data = Imgdir_Handler(img_urls).get_data()

    return data