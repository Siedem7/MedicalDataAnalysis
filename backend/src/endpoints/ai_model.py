import os
import pickle
from flask import jsonify, request, abort
from werkzeug.utils import secure_filename
from src.database_models import *
from src.functions import *
from src.ai_model import AI_model
from src.data_set import data_set


def create_model():
    """
    Creates model based on request. Model is then saved on local disk in
    order to reuse it.

    Request body should contain:
        - file_id: used to crated dataset,
        - model_name: name of model,
        - model_desc: description of model,
        - training_percent: (0-1) float value, indicating division
             between training and test sets,
        - categorical_columns: list of column names that should be converted to dummies,
        - numerical_columns: list of column names that should be normalized with min max values,
        - output_column: name of column considered as output values,
        - epochs: number of iteration of learning process
        - batch_size: size of batch processed at time in learning process
        - layers: list of layers.

        Layer structure:
        First layer consist of "output" and creates linear function by default. This
        behaviour cannot be changed. Each layer (different from first) within the
        "layers" array consists of the following attributes:

            "function" (required): Specifies the activation function or layer type to be used.
            Supported Activation Functions:
                "ReLU": Rectified Linear Unit activation function.
                "Tanh": Hyperbolic Tangent activation function.
                "Sigmoid": Sigmoid activation function.
                "Linear": Represents a linear layer.

            "input" (required for "Linear" layers): Specifies the number of input units for the layer.
            "output" (required for "Linear" layers): Specifies the number of output units for the layer.

    Endpoint: POST /create_model

    Requires:
    - Authorization header with a valid token
    - CREATE_MODEL permission

    Returns:
    - JSON object with text informing of model creation

    Error Responses:
    - 400 Bad Request: If data provided in request body are invalid
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    """
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token, ["CREATE_MODEL"])
    if status != 200:
        abort(status, result)

    expected_keys = ["file_id", "numerical_columns", "categorical_columns", "output_column", "epochs", "batch_size",
                     "model_name", "model_desc", "training_percent", "layers"]
    if not any(key in request.json.keys() for key in expected_keys):
        abort(400, description="Missing keys in the request.")

    file_id = request.json["file_id"]
    file = db.session.execute(db.select(File).filter_by(id=file_id)).scalar_one()
    file_path = file.path
    file_name = os.path.splitext(os.path.basename(file.path))[0]
    data_instance = data_set(name=file_name, description=file.description)
    data_instance.load_data(file_path=file_path)

    numerical_columns = request.json["numerical_columns"]
    categorical_columns = request.json["categorical_columns"]
    output_column = request.json["output_column"]
    epochs = request.json["epochs"]
    batch_size = request.json["batch_size"]

    data_instance.normalize_data(
        numerical_columns=numerical_columns,
        categorical_columns=categorical_columns,
        output_column=output_column
    )

    model_name = request.json["model_name"]
    model_description = request.json["model_desc"]
    training_percent = request.json["training_percent"]
    layers = request.json["layers"]

    model = AI_model(name=model_name, description=model_description)
    model.set_structure(data_instance, layers=layers)
    model.create_model(epochs, batch_size, training_percent)

    file_path = os.path.join(
        os.getcwd(), "model_files",
        secure_filename(model.name + ".pkl")
    )

    # Store the object to a file
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)

    model_database = PredictionModel()
    model_database.configuration = file_path
    model_database.modify_date = datetime.utcnow()
    model_database.user = result.id
    model_database.description = model.description
    model_database.name = model.name

    db.session.add(model_database)
    db.session.commit()
    return jsonify("Successfully created model.")


def get_models():
    token = request.headers.get("Authorization")
    status, result = authorize(token)

    if status != 200:
        abort(status, description=result)

    models = db.session.execute(db.select(PredictionModel)).scalars().all()
    return jsonify([{"name": model.name, "id": model.id} for model in models])