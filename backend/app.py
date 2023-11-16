from flask_cors import CORS
from flask import Flask,  jsonify, request, abort
from database_models import db, User

from functions import hash_password, validate_password, validate_email, generate_token, get_id_from_token

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)



CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

    with app.app_context():
        db.create_all()