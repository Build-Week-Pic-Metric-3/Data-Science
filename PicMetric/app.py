from flask import Flask, redirect, url_for


from .routes.summary import sum_bp
from .routes.batch_img_summary import bis_bp
from .models import DB

from decouple import config
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)
    app.register_blueprint(sum_bp)
    app.register_blueprint(bis_bp)

    @app.route('/')
    def redir():
        return redirect(url_for('reset'))

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return redirect(url_for('sum_bp.summary'))
    return app
