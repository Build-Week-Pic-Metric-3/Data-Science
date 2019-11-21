from flask import Flask, redirect, url_for, flash, request, render_template


from PicMetric.routes.do_data_science import do_data_science_bp
from PicMetric.routes.do_data_science_url import do_data_science_url_bp
from PicMetric.schema import DB
from flask_cors import CORS

import os
from decouple import config
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)
    
    app.register_blueprint(do_data_science_bp)
    app.register_blueprint(do_data_science_url_bp)

    @app.route('/')
    def redir():
        return redirect(url_for('upload'))


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return redirect(url_for('upload'))
    
    @app.route('/upload')
    def upload():
        return render_template('upload.html')

    return app