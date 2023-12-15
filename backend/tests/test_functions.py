import pytest
import hashlib
import jwt
from src.functions import hash_password, get_id_from_token, authorize, authorize_permissions, generate_token
from datetime import datetime, timedelta

# To run all tests type: pytest -v in command line
# To run single test type: pytest backend/tests/<test_file_name.py>::<test_function> in command line

@pytest.mark.parametrize("password", ["password", "otherpassword"])
def test_hash_password(password):
    """
    Test of hash_password method in functions.py
    """
    #GIVEN - password
    #WHEN
    hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
    #THEN
    assert hash_password(password) == hashed_password


#@pytest.mark.parametrize("password,result",[("haslospełniającekryteria",True),("haslo123",False)])
def test_validate_password():
    """
    Test of validate_password method in functions.py
    """
    #GIVEN
    #WHEN
    #THEN
    assert True


#@pytest.mark.parametrize("login, result", [("login1$", True), ("login", False), (" ", False)])
def test_validate_login():
    """
    Test of validate_login method in functions.py
    """
    #GIVEN
    #WHEN
    #THEN
    assert True

   
@pytest.mark.parametrize("test_token, expected_result", [(
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
def test_get_id_from_token(test_token, expected_result):
    """
    Test of get_id_from_token method in functions.py
    """
    #GIVEN test_token, expected result
    #WHEN
    result = get_id_from_token(test_token)
    #THEN
    assert result == expected_result


@pytest.mark.parametrize("test_id", [1, 10])
def test_generate_token(test_id):
    """
    Test of generate_token method in functions.py
    """
    #GIVEN test_id
    #WHEN
    result = generate_token(test_id)
    #THEN
    assert test_id == get_id_from_token(result)


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
    Test of authorize method in functions.py
    """
    #GIVEN - test_token, expected status, flask application
    #WHEN
    with app.app_context():
        #THEN
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
    Test of authorize_permissions method in functions.py
    """
    #GIVEN - test_token, permission, expected status, flask application
    #WHEN
    with app.app_context():
        #THEN
        assert authorize_permissions(test_token, permission)[0] == status
        

