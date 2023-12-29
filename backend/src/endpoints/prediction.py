import pickle
from flask import jsonify, request, abort
from src.database_models import *
from src.functions import *


def get_input_structure(model_id):
    """
    Receives dictionary representing data structure, needed to properly
    upload data to predict.

    Endpoint: GET /input_structure/<model_id>

    Requires:
    - Authorization header with a valid token
    - USE_MODEL permission

    Returns:
    - JSON file with list of users

    Error Responses:
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    - 404 Not Found: If model with given id does not exist

    """
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token, ["USE_MODEL"])

    if status != 200:
        abort(status, result)

    try:
        model_database = db.session.execute(db.select(PredictionModel).filter_by(id=model_id)).scalar_one()
    except NoResultFound:
        abort(404, description="Model with given id does not exist")

    with open(model_database.configuration, 'rb') as file:
        model = pickle.load(file)

    return jsonify(model.data.get_data_structure())