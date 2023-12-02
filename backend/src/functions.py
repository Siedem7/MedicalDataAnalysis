import hashlib
import re
import jwt
from datetime import datetime, timedelta
import secrets
import string
from sqlalchemy.exc import NoResultFound
from database_models import db, User, Group, Permission


# Only for development purposes
# For production use environment variables
SECRET_KEY = 'some key'


def hash_password(password):
    """
    Hash password using SHA512 algorithm. Used to store password 
    in database.

    Parameters: 
        password (str): plain password to hash.

    Returns:
        str: hashed password.
    """
    hashedPassword = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hashedPassword


# Check if password is valid
# Needs to be confirmed with passwords policy
def validate_password(password):
    """
    Check if password meets requirements configured in passwords 
    policy.

    Parameters: 
        password (str): plain password to check.

    Returns:
        bool: True if password meets requirements, False otherwise.
    """
    return True


# Check if login is valid
def validate_login(login):
    """
    Check if login meets requirements. (consists of letters, numbers, 
    special caracters)

    Parameters: 
        login (str): login to check.    
    
    Returns:
        bool: True if login meets requirements, False otherwise.
    """
    return re.search(r"^[a-zA-Z0-9_.-]+$", login)


def generate_token(user_id):
    """
    Generate authorization token (jwt) based on user id. Token is 
    valid for 1 day.

    Parameters: 
        user_id (int): id of user to generate token for.

    Returns:
        str: generated token.
    """

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


def get_id_from_token(token):
    """
    Extract user id from token. Used to authenticate user.

    Parameters:
        token (str): token to decode.

    Returns:
        int: user id.
    """
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
    """
    Authorize user based on token.
    
    Parameters:
        token (str): token to decode.

    Returns:
        int: status code.
        str: result message.
    """

    # Check if token is valid
    if token is None or token[:7] != "Bearer ":
        return 401, "Invalid token."

    # Extract user id from token
    user_id = get_id_from_token(token[7:])

    try:
        # Get user from database
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        # If user does not exist return 401
        return 401, "No user with provided token."
    
    # Return user, and ok status
    return 200, user


def authorize_permissions(token, permissions):
    """
    Authorize user based on token and permissions.

    Parameters:
        token (str): token to decode.
        permissions (list): list of permissions to check.

    Returns:
        int: status code.
        str: result message. 
    """
    
    # Authorize user based on token
    status, result = authorize(token)

    # If user is not authorized return status and result
    if status != 200:
        return status, result

    user = result

    # Check if user has specified permissions
    for permission in permissions:
        if permission not in [permission.name for permission in user.groups.permissions]:
            return 403, "No permission to access this feature."
    
    return 200, user


def initialize_database():
    """
    Initialize database with basic information. Used only for 
    development and tests.
    """
    user1 = User(login="admin",
                 password=hash_password("admin"),
                 password_expire_date=datetime.utcnow() + timedelta(days=30),
                 group=1)

    group1 = Group(name="admin")
    group2 = Group(name="analyst")
    group3 = Group(name="medical_staff")

    permission1 = Permission(name="DELETE_USER_ACCOUNT")
    permission2 = Permission(name="UPDATE_USER_ACCOUNT")
    permission3 = Permission(name="CREATE_USER_ACCOUNT")
    permission4 = Permission(name="MANAGE_PASSWORDS_POLICY")
    permission5 = Permission(name="CREATE_MODEL")
    permission6 = Permission(name="MANAGE_FILE")
    permission7 = Permission(name="VIEW_STATISTICS")
    permission8 = Permission(name="USE_MODEL")

    group1.permissions.append(permission1)
    group1.permissions.append(permission2)
    group1.permissions.append(permission3)
    group1.permissions.append(permission4)
    group2.permissions.append(permission5)
    group2.permissions.append(permission6)
    group2.permissions.append(permission7)
    group3.permissions.append(permission7)
    group3.permissions.append(permission8)

    db.session.add(user1)
    db.session.add_all([group1, group2, group3])
    db.session.add_all([permission1, permission2, permission3, permission4,
                        permission5, permission6, permission7, permission8])

    db.session.commit()
