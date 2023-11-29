import pytest
from src.app import create_app
from src.database_models import db
from datetime import datetime, timedelta
from src.functions import initialize_database


@pytest.fixture()
def app():
    app = create_app("sqlite://")
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()
        initialize_database()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()