from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from src.database_models import *
from src.functions import *


def get_users():
    """
    Retrieves list of registered users.

    Endpoint: GET /users

    Requires:
    - Authorization header with a valid token
    - DELETE_USER_ACCOUNT or UPDATE_USER_ACCOUNT permission

    Returns:
    - JSON file with list of users

    Error Responses:
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    """
    token = request.headers.get("Authorization")
    status, result = authorize(token)

    if status != 200:
        abort(status, description=result)

    required_permissions = ["DELETE_USER_ACCOUNT", "UPDATE_USER_ACCOUNT"]

    user_permissions = result.groups.permissions
    if not any(permission.name in required_permissions for permission in user_permissions):
        abort(403, "No permission to access this feature.")

    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify({"users": [{"login": user.login, "id": user.id} for user in users]})


def get_user(user_id):
    """
    Retrieves info about user.

    Endpoint: GET /user/<user_id>

    Requires:
    - Authorization header with a valid token
    - DELETE_USER_ACCOUNT or UPDATE_USER_ACCOUNT or CREATE_USER_ACCOUNT permission

    Returns:
    - JSON file with user data

    Error Responses:
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    - 404 No Found: User with provided id not found
    """
    token = request.headers.get("Authorization")
    status, result = authorize(token)

    if status != 200:
        abort(status, description=result)

    required_permissions = ["DELETE_USER_ACCOUNT", "UPDATE_USER_ACCOUNT", "CREATE_USER_ACCOUNT"]
    user_group = db.session().execute(db.select(Group).filter_by(id=result.group)).scalar_one()

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        abort(404, description="User with that id not found.")

    user_permissions = user_group.permissions
    if not any(permission.name in required_permissions for permission in user_permissions):
        abort(403, "No permission to access this feature.")

    user_info = {
        "login": user.login,
        "group": user.groups.name,
        "permissions": [permission.name for permission in user.groups.permissions]
    }
    return jsonify(user_info)


def login_user():
    """
    Logs user to server. Check if user with provided login and password exists,
    then returns generated token used for further authorization.

    Endpoint: POST /login

    Request Body:
    {
        "login": str,    # User login
        "password": str   # User password
    }

    Returns:
    - JSON object with token assigned to user

    Error Responses:
    - 404 No Found: If login or password is invalid
    """
    expected_keys = ["login", "password"]
    if not all(key in request.json.keys() for key in expected_keys):
        abort(400, description="Missing keys in the request")

    login = request.json["login"]
    password = request.json["password"]

    try:
        user = db.session.execute(
            db.select(User).filter_by(login=login, password=hash_password(password))).scalar_one()
    except NoResultFound:
        abort(404, description="Invalid login or password.")

    token = generate_token(user.id)
    return jsonify({"token": token})


def create_user():
    """
    Create user in database.

    Endpoint: POST /create_user

    Requires:
    - Authorization header with a valid token
    - CREATE_USER_ACCOUNT permission

    Request Body:
    {
        "login": str,    # User login
        "password": str,   # User password
        "group": str    # Group name
    }

    Returns:
    - JSON object with text informing of successful user creation

    Error Responses:
    - 400 Bad Request: If data provided in request body are invalid
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    - 409 Conflict: If login provided in request body is already in use
    """
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token, ["CREATE_USER_ACCOUNT"])

    if status != 200:
        abort(status, description=result)

    expected_keys = ["login", "password", "group"]
    if not all(key in request.json.keys() for key in expected_keys):
        abort(400, description="Missing keys in the request body")

    login = request.json["login"]
    password = request.json["password"]
    group_name = request.json["group"]

    if not validate_login(login):
        abort(400, description="Invalid login.")

    if not validate_password(password):
        abort(400, description="Password doesn't meet requirements.")

    # verify password with policy (length, special characters, etc.)
    try:
        group = db.session.execute(db.select(Group).filter_by(name=group_name)).scalar_one()
    except NoResultFound:
        abort(400, description="Invalid group name.")

    try:
        user = User(login=login,
                    password=hash_password(password),
                    password_expire_date=datetime.utcnow() + timedelta(days=30),
                    group=group.id)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        abort(409, description="User with that login already exists.")

    return jsonify("Successfully created user.")


def delete_user():
    """
    Delete user in database.

    Endpoint: DELETE /delete_user

    Requires:
    - Authorization header with a valid token
    - DELETE_USER_ACCOUNT permission

    Request Body:
    {
        "user_id": int  # User id
    }

    Returns:
    - JSON object with text informing of successful user deletion

    Error Responses:
    - 400 Bad Request: If data provided in request body are invalid
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    - 404 Not Found: If user with that id not found
    """
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token, ["DELETE_USER_ACCOUNT"])

    if status != 200:
        abort(status, description=result)

    if "user_id" not in request.json.keys():
        abort(400, description="Missing user_id in the request.")

    user_id = request.json["user_id"]

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        abort(404, description="User with that id not found.")

    db.session.delete(user)
    db.session.commit()

    return jsonify("Successfully deleted user.")


def update_user():
    """
    Update user in database.

    Endpoint: PUT /update_user

    Requires:
    - Authorization header with a valid token
    - UPDATE_USER_ACCOUNT permission

    Request Body:
    {
        "user_id": int,  # User id
        "password": str,   # User password
        "group": str    # Group name
    }

    Returns:
    - JSON object with text informing of successful user update

    Error Responses:
    - 400 Bad Request: If data provided in request body are invalid
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    - 404 Not Found: If user with that id not found
    - 409 Conflict: If login provided in request body is already in use
    """
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token, ["UPDATE_USER_ACCOUNT"])

    if status != 200:
        abort(status, description=result)

    if "user_id" not in request.json.keys():
        abort(400, "Missing user_id in request.")

    expected_keys = ["login", "password", "group"]
    if not any(key in request.json.keys() for key in expected_keys):
        abort(400, description="Missing keys in the request.")

    user_id = request.json["user_id"]

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        abort(404, description="User with that id not found.")

    if "login" in request.json:
        login = request.json["login"]

        if not validate_login(login):
            abort(400, description="Invalid login.")

        try:
            user.login = login
            db.session.commit()
        except IntegrityError:
            abort(409, description="Already used login.")

    if "group" in request.json:
        group_name = request.json["group"]

        try:
            group = db.session.execute(db.select(Group).filter_by(name=group_name)).scalar_one()
        except NoResultFound:
            abort(400, description="Invalid group name.")

        user.group = group.id

    if "password" in request.json:
        password = request.json["password"]

        if not validate_password(password):
            abort(400, description="Password doesn't meet requirements.")

        user.password = hash_password(password)
        user.password_expire_date = datetime.utcnow() + timedelta(days=30)

    db.session.commit()
    return jsonify("Successfully updated user.")