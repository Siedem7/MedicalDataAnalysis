from datetime import datetime,timedelta
import pytest
import os
from src.app import create_app
from src.functions import initialize_database, hash_password
from src.database_models import File, User, PredictionModel, db

@pytest.fixture()
def app():
    """
    Method creates flask application for testing purposes
    """
    app = create_app("sqlite://")
    app.config.update({
        "TESTING": True,
    })
    app.config["UPLOAD_FOLDER"] =  os.path.join(os.getcwd(), "data_files")

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.mkdir("./data_files")

    app.config["MODEL_FILES"] = os.path.join(os.getcwd(), "model_files")

    if not os.path.exists(app.config["MODEL_FILES"]):
        os.mkdir("./model_files")

    with app.app_context():
        db.create_all()
        initialize_database()

        database_file = File()
        database_file.description = "test"
        database_file.modify_date = datetime.utcnow()
        database_file.path = ".\\resources\\test_file.csv"
        database_file.user = 1

        analyst = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        
        medical_staff = User(login="medical_staff",
                password=hash_password("medical_staff"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=3)
        
        model = PredictionModel()
        model.configuration = ".\\resources\\test_model.pkl"
        model.modify_date = datetime.utcnow()
        model.user = 1
        model.description = "This model is for tests"
        model.name = "test_model"
        
        db.session.add(database_file)
        db.session.add(analyst)
        db.session.add(medical_staff)
        db.session.add(model)
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()