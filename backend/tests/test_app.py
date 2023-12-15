import shutil
import pytest
import jwt
from datetime import datetime, timedelta
from src.functions import generate_token
from pathlib import Path

resources = Path(__file__).parent / "resources"

# To run all tests type: pytest -v in command line
# To run single test type: pytest backend/tests/<test_file_name.py>::<test_function> in command line

@pytest.mark.parametrize("token, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 200),
    ("token", 401)])
def test_get_groups(token, statuscode, client, app):
    """
    Test of get_groups method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.get("/groups", headers={'Authorization': 'Bearer ' + token})
        #THEN
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
    Test of get_users method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.get("/users", headers={'Authorization': 'Bearer ' + token})
        #THEN
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
    Test of get_user method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.get("/user/"+ str(user_id), headers={'Authorization': 'Bearer ' + token})
        #THEN
        assert result.status_code == statuscode


@pytest.mark.parametrize("test_json, statuscode", [
    ({"login": "admin", "password": "admin"}, 200),
    ({"login": "user", "password": "123"}, 404)])
def test_login_user(test_json, statuscode, client):
    """
    Test of login_user method in app.py
    """
    #GIVEN - test_json, expected statuscode, test client
    #WHEN
    result = client.post("/login", json = test_json)
    #THEN
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
    Test of get_permissions method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.get("/permissions", headers={'Authorization': 'Bearer ' + token})
        #THEN
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
    Test of create_user method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.post("/create_user", headers={'Authorization': 'Bearer ' + token}, json = user_json)
        #THEN
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
    Test of delete_user method in app.py
    """
    #GIVEN
    with app.app_context():
        client.post("/create_user", headers={'Authorization': 'Bearer ' + generate_token(1)}, json = {"login": "login", "password": "admin", "group": "analyst"})
        #WHEN
        result = client.delete("/delete_user", headers={'Authorization': 'Bearer ' + token}, json = user_id)
        #THEN
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
    Test of update_user method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.put("/update_user", headers={'Authorization': 'Bearer ' + token}, 
                            json = parameter_json)
        #THEN
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
    Test of upload_file method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.post("/upload_file", headers={'Authorization': 'Bearer ' + token}, content_type='multipart/form-data',
                             data= user_data)
        #THEN
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
    Test of get_permissions method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.get("/get_datasets", headers={'Authorization': 'Bearer ' + token})
        #THEN
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
    Test of create_model method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.post("/create_model", headers={'Authorization': 'Bearer ' + token}, 
                             json = model)
        #THEN
        assert result.status_code == statuscode    


@pytest.mark.parametrize("token, model_id, statuscode", [
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 3
    }, 'some key', algorithm='HS256'), 1, 200),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 3
    }, 'some key', algorithm='HS256'), 10, 404),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 1, 403),
    ("token", 1, 401)])
def test_get_input_structure(token, model_id, statuscode, client, app):
    """
    Test of get_input_structure method in app.py
    """
    #GIVEN
    with app.app_context():
        #WHEN
        result = client.get("/input_structure/"+ str(model_id), headers={'Authorization': 'Bearer ' + token})
        #THEN
        assert result.status_code == statuscode     
   
def tearDownModule():
    shutil.rmtree("./backend/tests/resources/model_files")
    shutil.rmtree("./backend/tests/resources/data_files")