import os

from flask import Flask
from .BasicImageRead import *
from .Preprocess_image import main as main2
from .Preprocess_image import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Cards(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cardName: Mapped[str] = mapped_column(unique=False)
    setName: Mapped[str] = mapped_column(unique=False)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER='flaskr/User_Files/',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db',
        TEMPLATE_FOLDER = 'flaskr/templates/'
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .Upload_Image import upload
    app.register_blueprint(upload)

    from .database import database
    app.register_blueprint(database)

    return app


