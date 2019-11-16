from flask import Blueprint

sum_bp = Blueprint('sum_bp', __name__)

@sum_bp.route('/summary')
def summary():
    return 'summary'