from flask import Blueprint, request
from PicMetric.classes.img_handler import Img_Handler

bis_bp = Blueprint('bis_bp', __name__)

@bis_bp.route('/batch_img_summary')
def batch_img_summary():
    urls = [
        'https://i.redd.it/t5gqutndubs31.png',
        'https://i.redd.it/wutifutmubs31.jpg',
        'https://i.redd.it/5q7spoypubs31.jpg',
        'https://i.redd.it/a2koy4ptubs31.jpg',
        'https://i.redd.it/pk77o0u4vbs31.jpg'
    ]

    data = Img_Handler(urls).get_data()

    return data