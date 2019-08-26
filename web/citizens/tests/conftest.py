import pytest
from ...citizens.app import create_app
from ..database import db


@pytest.fixture(autouse=True)
def app():
    app = create_app(testing=True)
    return app


@pytest.yield_fixture(autouse=True)
def _init_db(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()
