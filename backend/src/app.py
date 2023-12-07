import csv
import os
import pickle

from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from flask_socketio import SocketIO, send, emit

from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

import datetime
from src.database_models import *
from src.functions import *

from src.ai_model import AI_model
from src.data_set import data_set


def create_app(database_uri="sqlite:///project.db"):
    """
    Creates app with specified database path. 

    Parameters: 
        database_uri (str): database name. 
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)
    socketio = SocketIO(app)

    app.config["UPLOAD_FOLDER"] =  os.path.join(os.getcwd(), "data_files")
    app.config["MODEL_FILES"] = os.path.join(os.getcwd(), "model_files")

    CORS(app)

    @app.route("/", methods=["GET"])
    def test():
        model_database = db.session.execute(db.select(PredictionModel).filter_by(id=1)).scalar_one()

        with open(model_database.configuration, 'rb') as file:
            model = pickle.load(file)


        print(model.data.data)
        print(model.data.get_data_structure())
        print(model.data.is_data_normalized)
        print(model.is_model_trained)

        return jsonify("taktak")

    @app.route("/groups", methods=["GET"]) 
    def get_groups():
        """ 
        Get list of groups defined in the system. Only available for logged users.

        Returns
            200, List of groups. 
            403, No permission to access this feature. (Not logged in).  
        """
        token = request.headers.get("Authorization")
        status, result = authorize(token)


        if status != 200:
            abort(status, description=result)

        groups = db.session.execute(db.select(Group)).scalars().all()
        return jsonify({"groups": [group.name for group in groups]})

    @app.route("/users", methods=['GET'])
    def get_users():
        """
        Get list of users registerd in the system. 

        Requires DELETE_USER_ACCOUNT or UPDATE_USER_ACCOUNT

        Returns:
            200, List of users.
            403, No permission to access this feature.
        """   
        token = request.headers.get("Authorization")
        status, result = authorize(token)

        if status != 200:
            abort(403, description=result)

        required_permissions = ["DELETE_USER_ACCOUNT", "UPDATE_USER_ACCOUNT"]
        
        user_permissions = result.groups.permissions
        if not any(permission.name in required_permissions for permission in user_permissions):
            abort(403, "No permission to access this feature.")

        users = db.session.execute(db.select(User)).scalars().all()
        return jsonify({"users": [{"login": user.login, "id": user.id} for user in users]})

    @app.route("/user/<int:user_id>", methods=["GET"])
    def get_user(user_id):

        """
        Get info by id about user registered in the system. 

        Requires DELETE_USER_ACCOUNT or UPDATE_USER_ACCOUNT or CREATE_USER_ACCOUNT

        Returns:
            200, Single user info.
            403, No permission to access this feature.
            404, User with that id not found
        """ 
        token = request.headers.get("Authorization")
        status, result = authorize(token)

        if status != 200:
            abort(403, description=result)

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
            "login" : user.login, 
            "group" : user.groups.name, 
            "permissions" : [permission.name for permission in user.groups.permissions]
        }
        return jsonify(user_info)

    @app.route("/login", methods=["POST"])
    def login_user():
        """
        Logs user to server. Check if user with provided login and password exists, 
        then returns generated token used for further authorization. 

        Request format: JSON

        Returns:
            200, Token in JSON format. 
            404, Invalid login or password.
        """
        login = request.json["login"]
        password = request.json["password"]

        try:
            user = db.session.execute(db.select(User).filter_by(login=login, password=hash_password(password))).scalar_one()
        except NoResultFound:
            abort(404, description="Invalid login or password.")

        token = generate_token(user.id)
        return jsonify({"token": token})

    @app.route("/permissions")
    def get_permissions():
        """
        Returns permission for user sending request based on authorization token.

        Request format: JSON
        
        Returns:
            200, Names of user permissions in JSON format. 
            403, No permission to access this feature. (Not logged in)
        """
        token = request.headers.get("Authorization")
        status, result = authorize(token)

        if status != 200:
            abort(status, description=result)

        user = result
        return jsonify({"permissions": [permission.name for permission in user.groups.permissions]})

    @app.route("/create_user", methods=["POST"])
    def create_user():
        """
        Create user in database. Request should have authorization header with token 
        used to authorize user and following information: 
            - login - user login
            - password - user password
            - group - name of user group

        Requires CREATE_USER_ACCOUNT permission.
        
        Request format: JSON
        
        Returns: 
            200, Successfully created user.
            400, Missing keys in the request. | Invalid login. | 
                 Passowrd doesn't meet requirements. | Invalid group name.
            403, No permission to access this feature.
            409, User with that login already exists.
        """
        token = request.headers.get("Authorization")
        status, result = authorize_permissions(token,["CREATE_USER_ACCOUNT"])

        if status != 200:
            abort(status, description=result)

        expected_keys = ["login", "password", "group"]
        if not all(key in request.json.keys() for key in expected_keys):
            abort(400, description="Missing keys in the request")

        login = request.json["login"]
        password = request.json["password"]
        group_name = request.json["group"]

        if not validate_login(login):
            abort(400, description="Invalid login.")

        if not validate_password(password):
            abort(400, description="Passowrd doesn't meet requirements.")

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

    @app.route("/delete_user", methods=["DELETE"])
    def delete_user():
        """
        Delete user in database. Request should have authorization header with token 
        used to authorize user and user_id (id of user to delete)
        
        Requires DELETE_USER_ACCOUNT permission.

        Request format: JSON
         
        Returns: 
            200, Successfully deleted user.
            400, Missing user_id in the request.
            403, No permission to access this feature.
            404, User with that id not found.
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

    @app.route("/update_user", methods=["PUT"])
    def update_user():
        """
        Update user in database. Request should have authorization header with token 
        used to authorize user, user_id (id of user to update) and at least one of 
        following information: 
            - login - new login
            - password - new password
            - group - name of new group

        Requires UPDATE_USER_ACCOUNT permission.

        Request format: JSON
        
        Returns: 
            200, Successfully updated user.
            400, Missing keys in the request. | Missing user_id in request.| Invalid group name.
            403, No permission to access this feature.
            404, User with that id not found.
            409, Already used login.
        """
        token = request.headers.get("Authorization")
        status, result = authorize_permissions(token, ["UPDATE_USER_ACCOUNT"])
        
        if status != 200:
            abort(status, description=result)

        if not "user_id" in request.json.keys():
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
            
            user.password = hash_password(password)
            user.password_expire_date=datetime.utcnow() + timedelta(days=30)

        db.session.commit()
        return jsonify("Successfully updated user.")

    @app.route("/upload_file", methods=["POST"])
    def upload_file():
        """
        Upload csv file containing data to system. Path with additional 
        infromations (description, upload data and owner) are also stored 
        in database. Request should have authorization header with token 
        used to authorize user and form-data body containing "csv_file" 
        and "description".

        Requires MANAGE_FILE permission.

        Request format: form-data
        
        Returns: 
            200, File uploaded succesfully
            400, Missing csv_file in request.
            403, No permission to access this feature. | Missing description in request.
            409, File with that name already exists on the server.
        """
        token = request.headers.get("Authorization")
        status, result = authorize_permissions(token, ["MANAGE_FILE"])

        if status != 200:
            abort(status, description=result)

        print( request.files.keys())
        if "csv_file" not in request.files.keys():
            abort(400, "Missing csv_file in request.")

        if "description" not in request.form.keys():
            abort(400, "Missing description in request.")

        date_uploaded = datetime.utcnow()

        new_file = request.files["csv_file"]
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"], 
            secure_filename(date_uploaded.strftime("%B %d %Y %H %M") + "_" + new_file.filename) 
        )

        if os.path.exists(file_path):
            abort(409, "File with that name already exists on the server.")

        new_file.save(file_path)

        database_file = File()
        database_file.description = request.form["description"]
        database_file.modify_date = date_uploaded
        database_file.path = file_path
        database_file.user = result.id

        db.session.add(database_file)
        db.session.commit()

        return jsonify("File uploaded succesfully")
    
    @app.route("/get_datasets", methods=["GET"])
    def get_datasets():
        """

        """
        token = request.headers.get("Authorization")
        status, result = authorize_permissions(token, ["MANAGE_FILE"])

        if status != 200:
            abort(status, result)

        
        files = db.session.execute(db.select(File)).scalars().all()
        
        datasets = list()
        for file in files:
            file_id = file.id      
            file_path = file.path
            file_description = file.description
            file_name = os.path.splitext(os.path.basename(file.path))[0]
            file_header = []
            with open(file_path, 'r') as file:
                csvreader = csv.reader(file)
                file_header = next(csvreader)

            datasets.append({"file_id": file_id, "file_name": file_name, "desc": file_description, "columns": file_header})
        
        return jsonify(datasets)

    @app.route("/create_model", methods=['POST']) 
    def create_model():
        """
        Creates model based on request. Model is then saved on local disk in 
        order to reuse it.  Request should have authorization header with 
        token used to authorize user and JSON body containing:
            - file_id: used to crated dataset,
            - model_name: name of model,
            - model_desc: description of model,
            - training_percent: (0-1) float value, indicating division 
                 between training and test sets,
            - categorical_columns: list of column names that shoud be converted to dummies,
            - numerical_columns: list of column names that should be normalized with min max values,
            - output_column: name of coulmn considered as output values,
            - epochs: number of iteration of learning process
            - batch_size: size of batch processed at time in learing process
            - layers: list of layers.

            Layer structure:
            First layer consist of "output" and creates linear function by default. This 
            behaviour cannot be changed. Each layer (different then first) within the 
            "layers" array consists of the following attributes:

                "function" (required): Specifies the activation function or layer type to be used.
                Supported Activation Functions:
                    "ReLU": Rectified Linear Unit activation function.
                    "Tanh": Hyperbolic Tangent activation function.
                    "Sigmoid": Sigmoid activation function.
                    "Linear": Represents a linear layer.
            
                "input" (required for "Linear" layers): Specifies the number of input units for the layer.

                "output" (required for "Linear" layers): Specifies the number of output units for the layer.    

        Requires CREATE_MODEL permission.

        Request format: JSON
        
        Returns: 
            200, Successfully created model.
            400, Missing keys in the request. | Invalid values.
            403, No permission to access this feature.
        """
        token = request.headers.get("Authorization")
        status, result = authorize_permissions(token, ["CREATE_MODEL"])
        if status != 200:
            abort(status, result)

        file_id = request.json["file_id"]
        file = db.session.execute(db.select(File).filter_by(id=file_id)).scalar_one()
        file_path = file.path
        file_name = os.path.splitext(os.path.basename(file.path))[0]
        data_instance = data_set(name=file_name, description=file.description)
        data_instance.load_data(file_path=file_path)

        numerical_columns =  request.json["numerical_columns"]
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
        model_descritpion = request.json["model_desc"]
        training_percent = request.json["training_percent"]
        layers = request.json["layers"]
        
        model = AI_model(name=model_name, description=model_descritpion)
        model.set_structure(data_instance, layers=layers)
        model.create_model(epochs, batch_size, training_percent, socketio)
    
        socketio.send(str(model.model))

        file_path = os.path.join( 
            app.config["MODEL_FILES"], 
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
        return jsonify("Succesfully crated model.")

    return app, socketio


if __name__ == "__main__":

    app, socketio = create_app()
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
    #app.run()
    
