from flask import Flask, redirect, url_for

from PicMetric.routes.do_data_science import do_data_science_bp

from decouple import config
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(do_data_science_bp)

    @app.route('/')
    def redir():
        return redirect(url_for('do_data_science_bp.do_data_science'))

    return app
