import os

from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from sqlalchemy.exc import NoResultFound, ArgumentError, IntegrityError

from database_models import *
from ai_model import AI_model
from data_set import data_set

import datetime
from datetime import timedelta, datetime
from functions import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

CORS(app)


@app.route("/")
def hello_world():
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

    login = request.json["login"]
    password = request.json["password"]
    group_id = request.json["group"]
    try:
        user = User(login=login,
                    password=hash_password(password),
                    password_expire_date=datetime.utcnow() + timedelta(days=30),
                    group=group_id)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        abort(409, description="User with that login already exists.")

    return jsonify("Successfully created user")


@app.route("/delete_user", methods=["POST"])
def delete_user():
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token,["DELETE_USER_ACCOUNT"])

    if status != 200:
        abort(status, description=result)

    id = request.json["id"]
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
        db.session.delete(user)
        db.session.commit()
    except IntegrityError:
        abort(409, description="User with that login already don't exists.")

    return jsonify("Successfully deleted user")

@app.route("/update_user", methods=["POST"])
def update_user():
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token,["UPDATE_USER_ACCOUNT"])

    if status != 200:
        abort(status, description=result)

    id = request.json["id"]
    new_role_id = request.json["new_role_id"]
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
        user.group=new_role_id
        db.session.commit()
    except IntegrityError:
        abort(409, description="User with that login already don't exists.")

    return jsonify("Successfully updated user")


if __name__ == "__main__":
    isInitialized = bool(os.path.exists("./instance/project.db"))

    with app.app_context():
        db.create_all()

        if not isInitialized:
            initialize_database()

    app.run()
