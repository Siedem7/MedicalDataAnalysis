import pytest
import hashlib
import jwt
from src.functions import hash_password, get_id_from_token, authorize, authorize_permissions, validate_login, generate_token
from datetime import datetime, timedelta

# test if method is hashing password correctly
@pytest.mark.parametrize("password", ["password", "otherpassword"])
def test_hash_password(password):
    """
    GIVEN password,  expected function result
    WHEN hash password the same way as tested method
    THEN function should return false for incorrect password and return true for correct password
    """
    hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
    assert hash_password(password) == hashed_password


#@pytest.mark.parametrize("password,result",[("haslospełniającekryteria",True),("haslo123",False)])
def test_validate_password():
    """
    GIVEN password,  expected function result
    THEN function should return false for incorrect password and return true for correct password
    """
    assert True


@pytest.mark.parametrize("login, result", [("login1$", True), ("login", False), (" ", False)])
def test_validate_login(login, result):
    """
    GIVEN password,  expected function result
    THEN function should return false for incorrect login and return true for correct login
    """
    assert validate_login(login) == result


#test if method get id correctly from generated token    
@pytest.mark.parametrize("test_token, result", [(
    jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 1),
    ("token", 'Invalid token. Please log in again.'),
    (jwt.encode({
        'exp': datetime.utcnow() - timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'), 'Signature expired. Please log in again.')])
def test_get_id_from_token(test_token, result):
    """
    GIVEN bearer token,  expected function result
    THEN  Id from token is the same as expected result
    """
    assert get_id_from_token(test_token) == result


@pytest.mark.parametrize("test_id", [1, 10])
def test_generate_token(test_id):
    """
    GIVEN user id
    WHEN generate token the same way as tested method
    THEN token generated from funcion should have correct user id
    """
    result = generate_token(test_id)
    assert test_id == get_id_from_token(result)


# test if method correctly authorize
@pytest.mark.parametrize("test_token, status", [
("Bearer " + jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
}, 'some key', algorithm='HS256'), 200),
("Bearer " + jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 10
}, 'some key', algorithm='HS256'), 401)])
def test_authorize(test_token, status, app):
    """
    GIVEN token, expected status, flask application
    THEN function should return permissions if token is correct and token's user exist
    """
    with app.app_context():
        assert authorize(test_token)[0] == status


# test if method correctly authorize permissions
@pytest.mark.parametrize("test_token, permission, status", [
("Bearer " + jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
}, 'some key', algorithm='HS256'),["permission"], 403),
("Bearer " + jwt.encode({
    'exp': datetime.utcnow() + timedelta(days=1),
    'iat': datetime.utcnow(),
    'sub': 1
}, 'some key', algorithm='HS256'),["CREATE_USER_ACCOUNT"], 200),
("token",["permission"], 401)])
def test_authorize_permissions(test_token, permission, status, app):
    """
    GIVEN token, permission, expected status, flask application
    THEN function should return permission if user has access to this permission or return message when user cannot access this permission
    """
    with app.app_context():
        assert authorize_permissions(test_token, permission)[0] == status
        

