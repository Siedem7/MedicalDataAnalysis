import csv
import os
import pickle

from flask_cors import CORS
from flask import Flask, jsonify, request, abort
from flask_socketio import SocketIO, send, emit

from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

import datetime
from src.database_models import *
from src.endpoints import group, user, permissions, file, prediction, ai_model
from src.functions import *
from src.socketio_functions import socketio


def create_app(database_uri="sqlite:///project.db"):
    """
    Creates app with specified database path. 

    Parameters: 
        database_uri (str): database name. 
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)
    socketio.init_app(app)

    CORS(app)

    app.add_url_rule("/groups", methods=["GET"], view_func=group.get_groups)
    app.add_url_rule("/users", methods=["GET"], view_func=user.get_users)
    app.add_url_rule("/user/<user_id>", methods=["GET"], view_func=user.get_user)
    app.add_url_rule("/login", methods=["POST"], view_func=user.login_user)
    app.add_url_rule("/create_user", methods=["POST"], view_func=user.create_user)
    app.add_url_rule("/delete_user", methods=["DELETE"], view_func=user.delete_user)
    app.add_url_rule("/update_user", methods=["PUT"], view_func=user.update_user)
    app.add_url_rule("/permissions", methods=["GET"], view_func=permissions.get_permissions)
    app.add_url_rule("/upload_file", methods=["POST"], view_func=file.upload_file)
    app.add_url_rule("/get_datasets", methods=["GET"], view_func=file.get_datasets)
    app.add_url_rule("/input_structure/<model_id>", methods=["GET"], view_func=prediction.get_input_structure)
    app.add_url_rule("/create_model", methods=["POST"], view_func=ai_model.create_model)
    app.add_url_rule("/models", methods=["GET"], view_func=ai_model.get_models)

    return app


if __name__ == "__main__":
    app = create_app()
    isInitialized = os.path.exists("src/instance/project.db")
    if not os.path.exists("data_files"):
        os.mkdir("data_files")

    if not os.path.exists("model_files"):
        os.mkdir("model_files")

    with app.app_context():
        db.create_all()

        if not isInitialized:
            initialize_database()
    socketio.run(app)
