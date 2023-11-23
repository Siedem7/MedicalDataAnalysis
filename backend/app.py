from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from sqlalchemy.exc import NoResultFound, ArgumentError, IntegrityError

from database_models import *

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
                    password_expire_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
                    group=group_id)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        abort(409, description="User with that login already exists.")

    return jsonify("Successfully created user")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        user1 = User(login="admin",
                     password=hash_password("admin"),
                     password_expire_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
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
    app.run()
