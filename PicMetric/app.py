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
bucket_name = S3_BUCKET

S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)




load_dotenv()

import boto3, botocore

s3 = boto3.client(
   "s3",
   aws_access_key_id= S3_KEY,
   aws_secret_access_key= S3_SECRET
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'PicMetric/assets/temp/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION, file.filename)




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
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            s3_path = upload_file_to_s3(f, S3_BUCKET)
            return 'file uploaded successfully'
    return app