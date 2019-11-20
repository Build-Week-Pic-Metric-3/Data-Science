from flask import Flask, redirect, url_for, flash, request, render_template
from werkzeug.utils import secure_filename

from PicMetric.routes.do_data_science import do_data_science_bp
from PicMetric.schema import DB
from flask_cors import CORS

import os
from decouple import config
from dotenv import load_dotenv


S3_BUCKET = config('S3_BUCKET')
S3_KEY = config('S3_KEY')
S3_SECRET = config('S3_SECRET')

load_dotenv()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'PicMetric/assets/temp/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)
    
    app.register_blueprint(do_data_science_bp)

    @app.route('/')
    def redir():
        return redirect(url_for('do_data_science_bp.do_data_science'))


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return 'DataBase Reset Successful'
    
    @app.route('/upload')
    def upload_file_form():
        return render_template('upload.html')

    @app.route('/uploader', methods = ['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return 'file uploaded successfully'
    return app