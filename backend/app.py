import datetime

from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from sqlalchemy.exc import NoResultFound

from database_models import db, User

from functions import hash_password, validate_password, validate_email, generate_token, get_id_from_token

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
    if token is None or token[:7] != "Bearer ":
        abort(401, description="Invalid token.")

    user_id = get_id_from_token(token[7:])

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one()
    except NoResultFound:
        abort(401, description="No user with provided token.")

    return jsonify({"permissions": [permission.name for permission in user.groups.permissions]})


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
