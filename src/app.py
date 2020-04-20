from flask import Flask
from flask_sqlalchemy import SQLAlchemy   

from config import config
from src.router import route_app

from src.extensions import db

import mimetypes


def create_app(config_name):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    route_app(app)
    import src.orm_models
    app.cli.add_command(src.orm_models.init_db_command)

    #Fix mimetype issue
    mimetypes.add_type('text/javascript', '.js')

    return app
    