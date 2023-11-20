import datetime


from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from sqlalchemy.exc import NoResultFound, ArgumentError, IntegrityError

from database_models import db, User

from functions import hash_password, validate_password, validate_email, generate_token, get_id_from_token, authorize, \
    authorize_permissions

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
        user =User(login=login,
              password=hash_password(password),
              password_expire_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
              group=group_id)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        abort(409, description="User with that login already exists.")

    return jsonify("Successfuly created user")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        try:
            admin = db.session.execute(db.select(User).filter_by(login="admin")).scalar_one()
        except NoResultFound:
            password = hash_password("admin")
            admin = User(login="admin",
                         password=password,
                         password_expire_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
                         group=1)
            db.session.add(admin)
            db.session.commit()
    app.run()
