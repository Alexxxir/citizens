import os
from flask import Flask

from .database import db
from .config import DevelopmentConfig, ProductionConfig


def create_app(development=True):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig if development else ProductionConfig)

    db.init_app(app)

    from .citizens.module import module as citizens

    app.register_blueprint(citizens)
    return app
