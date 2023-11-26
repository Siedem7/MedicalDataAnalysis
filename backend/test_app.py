import pytest
from app import *
from functions import *
from flask import jsonify

#pytest -v

@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture()
def runner():
    return app.test_cli_runner()


def test_home(client):
    response = client.get("/")
    assert b'Hello World!' in response.data


def test_login_user(client):
    token = client.post("/login",json={"login": "admin","password": "admin"})
    user_id = get_id_from_token(token.json["token"])
    assert user_id == 1


def test_get_permissions(client):    
    token = generate_token(1)
    permissions = client.get("/permissions", headers={'Authorization': 'Bearer ' + token}) 
    assert permissions.json["permissions"] == ['DELETE_USER_ACCOUNT', 'UPDATE_USER_ACCOUNT', 'CREATE_USER_ACCOUNT', 'MANAGE_PASSWORDS_POLICY']


def test_create_user(client):
    token = generate_token(1)
    user = client.post("/create_user",headers={'Authorization': 'Bearer ' + token},json={"login": "kamil","password": "admin","group": 1})
    try:
        new_user = db.session.execute(db.select(User).filter_by(login="kamil")).scalar_one()
        db.session.delete(new_user)
        db.session.commit()
    except IntegrityError:
        abort(409, description="Something went wrong")
    assert b'"Successfully created user"\n' in user.data
