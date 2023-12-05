import unittest
import pytest
import hashlib
import jwt
from src.functions import hash_password, get_id_from_token, authorize, authorize_permissions
from datetime import datetime, timedelta
from sqlalchemy.exc import NoResultFound
from src.database_models import db,User

#python -m tests.test_functions
class tests(unittest.TestCase):

    # test if method is hashing password correctly
    @pytest.mark.parametrize("password",["password","otherpassword"])
    def test_hash_password(password,self):
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        self.assertEqual(hash_password(password), hashed_password, "Wrong hashing!")

    #@pytest.mark.parametrize("password,result",[("haslospełniającekryteria",True),("haslo123",False)])
    def test_validate_password(self):
        assert True

    @pytest.mark.parametrize("login,result",[("login1$",True),("login",False),(" ",False)])
    def test_validate_login(self):
        assert True   

    @pytest.mark.parametrize("test_id,result_token",[(1,jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256')),(10,jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 10
    }, 'some key', algorithm='HS256'))])
    def test_generate_token(test_id,result_token,self):
        self.assertEqual(result_token, get_id_from_token(test_id), "Token was generated incorrectly")

    # test if method get id correctly from generated token
    @pytest.mark.parametrize("test_token,result",[(
        jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': 1
        }, 'some key', algorithm='HS256'),1),
        ("token",'Invalid token. Please log in again.'),
        (jwt.encode({
            'exp': datetime.utcnow() - timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': 1
        }, 'some key', algorithm='HS256'),'Signature expired. Please log in again.')])
    def test_get_id_from_token(test_token,result,self):
        self.assertEqual(result, get_id_from_token(test_token), "Function returned wrong user_id!")
 
    
    # test if method correctly authorize
    @pytest.mark.parametrize("test_token,status",[(
    jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),200),
    ((jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 10
    }, 'some key', algorithm='HS256')),401),
    ("token",401)])
    def test_authorize(test_token,status,self,app):
        with app.app_context():
            self.assertEqual(status,authorize(test_token)[0],"Something went wrong")


    # test if method correctly authorize permissions
    @pytest.mark.parametrize("test_token,permission,status",[(jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),["permission"],403),
    (jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': 1
    }, 'some key', algorithm='HS256'),["CREATE_USER_ACCOUNT"],200),
    ("token",["permission"],401)])
    def test_authorize_permissions(test_token,permission,status,self,app):
        with app.app_context():
            self.assertEqual(status, authorize_permissions(test_token, permission)[0],"Wrong return")


suite = unittest.TestLoader().loadTestsFromTestCase(tests)
unittest.TextTestRunner(verbosity=2).run(suite)
