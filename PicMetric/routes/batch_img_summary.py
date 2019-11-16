from flask import Blueprint

bis_bp = Blueprint('bis_bp', __name__)

@bis_bp.route('/batch_img_summary')
def batch_img_summary():
    return 'batch_img_summary'