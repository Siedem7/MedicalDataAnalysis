import hashlib
import re
import jwt
from datetime import datetime, timedelta
import secrets
import string
from sqlalchemy.exc import NoResultFound
from database_models import db, User, Group, Permission

# USE PYDOC TO GENERATE DOCUMENTATION
# CHANGE TEMPORARY COMMENTS TO DOCSTRINGS

# Only for development purposes
# For production use environment variables
SECRET_KEY = 'some key'


# Hash user password to store in database
def hash_password(password):
    hashedPassword = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashedPassword


# Check if password is valid
# Needs to be confirmed with passwords policy
def validate_password(password):
    return True


# Check if email is valid
# Uses regex
def validate_email(email):
    return re.search(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@" +
                     r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email)


# Generate authorization token (jwt)
# Token contains user id
# Token is valid for 1 day
def generate_token(user_id):
    # Token data
    # exp - expiration date
    # iat - issued at
    # sub - subject (user id)
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }

    # Encode token based on data and secret key
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # Return generated token
    return token


# Extract user id from token
def get_id_from_token(token):
     # Decode token based on secret key 
     # Use try except to handle exceptions (invalid token, expired token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def authorize(token):
    if token is None or token[:7] != "Bearer ":
        return (401, "Invalid token.")

    user_id = get_id_from_token(token[7:])

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        return (401, "No user with provided token.")
    
    return (200, user)


def authorize(token, permissions):
    if token is None or token[:7] != "Bearer ":
        return (401, "Invalid token.")

    user_id = get_id_from_token(token[7:])

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        return (401, "No user with provided token.")
    
    for permission in permissions:
        if permission not in [permission.name for permission in user.groups.permissions]:
            return (403, "No permission to access this feature.")
    
    return (200, user)