import os

from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename


import datetime
from src.database_models import *
from src.functions import *


def create_app(database_uri="sqlite:///project.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)

    app.config["UPLOAD_FOLDER"] =  os.path.join(os.getcwd(), "data_files")

    CORS(app)

    @app.route("/")
    def hello_world():
        request.json['test']
        return "Hello World!"

    @app.route("/login", methods=["POST"])
    def login_user():
        login = request.json["login"]
        password = request.json["password"]

        try:
            user = db.session.execute(db.select(User).filter_by(login=login, password=hash_password(password))).scalar_one()
        except NoResultFound:
            abort(400, description="Invalid login or password.")

        token = generate_token(user.id)
        return jsonify({"token": token})

    @app.route("/permissions")
    def get_permissions():
        token = request.headers.get("Authorization")
        status, result = authorize(token)

        if status != 200:
            abort(status, description=result)

        user = result
        return jsonify({"permissions": [permission.name for permission in user.groups.permissions]})

    @app.route("/create_user", methods=["POST"])
    def create_user():
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

        return jsonify("Successfully created user")

    @app.route("/delete_user", methods=["DELETE"])
    def delete_user():
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

        return jsonify("Successfully deleted user")

    @app.route("/update_user", methods=["PUT"])
    def update_user():
        token = request.headers.get("Authorization")
        status, result = authorize_permissions(token, ["UPDATE_USER_ACCOUNT"])
        
        
        if status != 200:
            abort(status, description=result)

        expected_keys = ["user_id", "login", "password", "group"]
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
            password = request.json["group"]
            
            user.password = hash_password(password)
            user.password_expire_date=datetime.utcnow() + timedelta(days=30)

        
        db.session.commit()
        return jsonify("Successfully updated user")

    
    @app.route("/upload_file", methods=["POST"])
    def upload_file():
        """
        Upload csv file containing data to system. Path with additional 
        infromations (description, upload data and owner) are also stored 
        in database. Request should have authorization header with token 
        used to authorize user and form-data body containing "csv_file" 
        and "description".

        Requires MANAGE_FILE permission.

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

    return app


if __name__ == "__main__":

    app = create_app()
    isInitialized = os.path.exists("src/instance/project.db")
    if not os.path.exists("data_files"):
        os.mkdir("data_files")

    with app.app_context():
        db.create_all()

        if not isInitialized:
            initialize_database()

    app.run()
