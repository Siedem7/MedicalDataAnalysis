import pytest
import jwt
from datetime import datetime, timedelta
from src.functions import generate_token, hash_password
from src.database_models import db, User
from pathlib import Path

resources = Path(__file__).parent / "resources"

# pytest -v
@pytest.mark.parametrize("token, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 200),
    ("token", 401)])
def test_get_groups(token, statuscode, client, app):
    """
    GIVEN user token, expected status, test client, flask application
    WHEN get groups from database
    THEN function should return json with groups if token is correct
    """
    with app.app_context():
        result = client.get("/groups", headers={'Authorization': 'Bearer ' + token})
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), 403),
    ("token", 401)])
def test_get_users(token, statuscode, client, app):
    """
    GIVEN user token, expected status, test client, flask application
    WHEN get registerd users from database
    THEN function should return json with users if token is correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.get("/users", headers={'Authorization': 'Bearer ' + token})
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, user_id, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 1, 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), 1, 403),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 10, 404),
    ("token", 1, 401)])    
def test_get_user(token, user_id, statuscode, client, app):
    """
    GIVEN user token, user_id, expected status, test client, flask application
    WHEN get user info from database
    THEN function should return json with user info if token is correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.get("/user/"+ str(user_id), headers={'Authorization': 'Bearer ' + token})
    assert result.status_code == statuscode


@pytest.mark.parametrize("test_json, statuscode", [
    ({"login": "admin", "password": "admin"}, 200),
    ({"login": "user", "password": "123"}, 404)])
def test_login_user(test_json, statuscode, client):
    """
    GIVEN json with login and password, expected status, test client
    WHEN entered data to server
    THEN function should generate token if login and password are correct
    """
    result = client.post("/login", json = test_json)
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 10
    }, 'some key', algorithm='HS256'), 401),
    ("token", 401)])
def test_get_permissions(token, statuscode, client, app):
    """
    GIVEN bearer token, expected status, test client, flask application
    WHEN authorize token
    THEN function should return user's permissions if token is correct
    """
    with app.app_context():
        result = client.get("/permissions", headers={'Authorization': 'Bearer ' + token})
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, user_json, statuscode",[(jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),{"login": "login", "password": "admin", "group": "medical_staff"}, 200), 
    ("token",{"login": "kamil", "password": "admin", "group": "medical_staff"}, 401),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),{"login": "kamil", "password": "admin"},400),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),{"login": "admin", "password": "admin", "group": "admin"}, 409),    
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'),{"login": "admin", "password": "admin", "group": "admin"}, 403)])
def test_create_user(token, user_json, statuscode, client, app):
    """
    GIVEN token, json with user data, expected status, test client, flask application
    WHEN entered token and user data to server
    THEN function should create new user if token has permission to create user and user data is correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.post("/create_user", headers={'Authorization': 'Bearer ' + token}, json = user_json)
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, user_id, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2}, 200), 
    ("token",{"user_id": 2}, 401),     
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 10}, 404),    
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), {"id": 1}, 400),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), {"user_id": 2}, 403)])
def test_delete_user(token, user_id, statuscode, client, app):
    """
    GIVEN token, user id , expected status, test client, flask application
    WHEN create user and enter token and user id to delete
    THEN function should delete user with entered id if token has permission to delete user and user id is correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        client.post("/create_user", headers={'Authorization': 'Bearer ' + generate_token(1)}, json = {"login": "login", "password": "admin", "group": "analyst"})
        result = client.delete("/delete_user", headers={'Authorization': 'Bearer ' + token}, json = user_id)
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, parameter_json, statuscode",[ 
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2, "login": "newlogin"}, 200),
    ("token",{"user_id": 2}, 401),
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"id": 2}, 400),
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 10, "login": "newlogin"}, 404),    
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2}, 400),
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2, "login": ""}, 400),    
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2, "group": "1"}, 400),    
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2, "login": "admin"}, 409),
    (jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
    }, 'some key', algorithm='HS256'), {"user_id": 2, "password": "1"}, 400),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), {"user_id": 2, "login": "newlogin"}, 403)])
def test_update_user(token, parameter_json, statuscode, client, app):
    """
    GIVEN token, parameter to update , expected status, test client, flask application

    WHEN create user and enter token and user parameter to update

    THEN function should update user's parameters if token has permission to update user and entered parameters are correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.put("/update_user", headers={'Authorization': 'Bearer ' + token}, 
                            json = parameter_json)
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, user_data, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'),{"csv_file": (resources / "test_file.csv").open("rb"), "description": "description"}, 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),{"csv_file": "file", "description": "description"}, 403), 
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'),{"csv_file": "file"}, 400),
    ("token",{"csv_file": "file", "description": "description"}, 401)])
def test_upload_file(token, user_data, statuscode, client, app):
    """
    GIVEN token, file and description, expected status, test client, flask application

    WHEN upload file to database

    THEN function should upload file if token and entered data are correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.post("/upload_file", headers={'Authorization': 'Bearer ' + token}, content_type='multipart/form-data',
                             data= user_data)
    assert result.status_code == statuscode



@pytest.mark.parametrize("token, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 403),
    ("token", 401)])
def test_get_datasets(token, statuscode, client, app):
    """
    GIVEN token, expected status, test client, flask application

    WHEN get datasets from database

    THEN function should return datasets from database if token is correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.get("/get_datasets", headers={'Authorization': 'Bearer ' + token})
    assert result.status_code == statuscode


@pytest.mark.parametrize("token, model, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), {"file_id": 1}, 400),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), {"file_id": 1}, 403),
    ("token", {"file_id": 1}, 401),    
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'),{
    "file_id": 1, 
    "model_name": "Model gamma",
    "model_desc": "Testowanie",
    "training_percent": 0.8,
    "numerical_columns":[
            "age",
            "hypertension",
            "heart_disease",
            "avg_glucose_level",
            "bmi"
        ],
    "categorical_columns": [
            "gender",
            "ever_married",
            "work_type",
            "Residence_type",
            "smoking_status"
        ],
    "output_column":"stroke",
    "layers": [
            {"output":10}, 
            {"function":"ReLU"},
            {"function": "Linear", "input":10, "output":8},
            {"function": "Tanh"},
            {"function": "Linear", "input": 8, "output":1},
            {"function": "Sigmoid"}
    ],
    "epochs": 50,
    "batch_size": 100}, 200)])
def test_create_model(token, model, statuscode, client, app):
    """
    GIVEN token, model in JSON format, expected status, test client, flask application

    WHEN create and add model to database

    THEN function should create and add model if token and entered data are correct
    """
    with app.app_context():
        user = User(login="analyst",
                password=hash_password("analyst"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=2)
        db.session.add(user)
        db.session.commit()
        result = client.post("/create_model", headers={'Authorization': 'Bearer ' + token}, 
                             json = model)
    assert result.status_code == statuscode    


@pytest.mark.parametrize("token, model_id, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), 1, 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 2
    }, 'some key', algorithm='HS256'), 10, 404),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 1, 403),
    ("token", 1, 401)])
def test_get_input_structure(token, model_id, statuscode, client, app):
    """
    GIVEN token, model id, expected status, test client, flask application

    WHEN get input structure

    THEN function should return input structure if token is correct and model exists
    """
    with app.app_context():
        user = User(login="medical_staff",
                password=hash_password("medical_staff"),
                password_expire_date=datetime.utcnow() + timedelta(days=30),
                group=3)
        db.session.add(user)
        db.session.commit()
        result = client.get("/input_structure/"+ str(model_id), headers={'Authorization': 'Bearer ' + token})
    assert result.status_code == statuscode     
   