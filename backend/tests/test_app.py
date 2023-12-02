from flask import abort
from sqlalchemy.exc import IntegrityError
from src.functions import *


# pytest -v

def test_home(client, app):
    response = client.get("/")
    assert b'Hello World!' in response.data


def test_login_user(client, app):
    token = client.post("/login", json={"login": "admin", "password": "admin"})
    user_id = get_id_from_token(token.json["token"])
    assert user_id == 1


def test_get_permissions(client, app):
    token = generate_token(1)
    with app.app_context():
        permissions = client.get("/permissions", headers={'Authorization': 'Bearer ' + token})
    assert permissions.json["permissions"] == ['DELETE_USER_ACCOUNT', 'UPDATE_USER_ACCOUNT', 'CREATE_USER_ACCOUNT', 'MANAGE_PASSWORDS_POLICY']


def test_create_user(client, app):
    token = generate_token(1)
    with app.app_context():
        user = client.post("/create_user", headers={'Authorization': 'Bearer ' + token}, json={"login": "kamil", "password": "admin", "group": 1})
        try:
            new_user = db.session.execute(db.select(User).filter_by(login="kamil")).scalar_one()
            db.session.delete(new_user)
            db.session.commit()
        except NoResultFound:
            assert False
    assert b'"Successfully created user"\n' in user.data


def test_delete_user():
    assert True

def test_update_user():
    assert True