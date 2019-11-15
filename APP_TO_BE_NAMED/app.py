from flask import Flask, redirect, url_for

from .routes.summary import sum_bp
from .routes.batch_img_summary import bis_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(sum_bp)
    app.register_blueprint(bis_bp)

    @app.route('/')
    def redir():
        return redirect(url_for('sum_bp.summary'))

    return app
