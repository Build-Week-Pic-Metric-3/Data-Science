from flask import Flask, redirect, url_for

from PicMetric.routes.do_data_science import do_data_science_bp
from PicMetric.schema import DB
from flask_cors import CORS


from decouple import config
from dotenv import load_dotenv

load_dotenv()
logging.getLogger('flask_cors').level = logging.DEBUG

def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'*')

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
    return app
