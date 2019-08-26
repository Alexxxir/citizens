import os
from flask import Flask

from .database import db
from .config import DevelopmentConfig, ProductionConfig, TestingConfig


def create_app(development=True, testing=False):
    app = Flask(__name__)
    config = DevelopmentConfig
    if not development:
        config = ProductionConfig
    if testing:
        config = TestingConfig
    app.config.from_object(config)

    db.init_app(app)

    from .citizens.module import module as citizens

    app.register_blueprint(citizens)
    return app
