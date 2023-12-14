from datetime import datetime
import pytest
import os
from src.app import create_app
from src.database_models import db
from src.functions import initialize_database
from src.database_models import File

@pytest.fixture()
def app():
    app,socket = create_app("sqlite://")
    app.config.update({
        "TESTING": True,
    })
    app.config["UPLOAD_FOLDER"] =  os.path.join(os.getcwd(), "backend", "tests", "data_files")

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.mkdir("./backend/tests/data_files")

    app.config["MODEL_FILES"] = os.path.join(os.getcwd(), "backend", "tests", "model_files")

    if not os.path.exists(app.config["MODEL_FILES"]):
        os.mkdir("./backend/tests/model_files")

    with app.app_context():
        db.create_all()
        initialize_database()

        database_file = File()
        database_file.description = "test"
        database_file.modify_date = datetime.utcnow()
        database_file.path = ".\\backend\\tests\\resources\\test_file.csv"
        database_file.user = 1

        db.session.add(database_file)
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()