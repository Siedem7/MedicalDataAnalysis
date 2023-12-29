from flask import jsonify, request, abort
from src.functions import *


def get_permissions():
    """
    Retrieves list of permissions.

    Endpoint: GET /permissions

    Requires:
    - Authorization header with a valid token

    Returns:
    - JSON file with list of permissions

    Error Responses:
    - 403 Forbidden: If user is not logged in
    """
    token = request.headers.get("Authorization")
    status, result = authorize(token)

    if status != 200:
        abort(status, description=result)

    user = result
    return jsonify({"permissions": [permission.name for permission in user.groups.permissions]})