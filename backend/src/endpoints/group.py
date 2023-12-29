from flask import jsonify, request, abort
from src.functions import *


def get_groups():
    """
    Retrieves list of defined groups.

    Endpoint: GET /groups

    Requires:
    - Authorization header with a valid token

    Returns:
    - JSON file with list of groups.

    Error Responses:
    - 403 Forbidden: If user is not logged in
    """
    token = request.headers.get("Authorization")
    status, result = authorize(token)

    if status != 200:
        abort(status, description=result)

    groups = db.session.execute(db.select(Group)).scalars().all()
    return jsonify({"groups": [group.name for group in groups]})