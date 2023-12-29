import csv
import os
from flask import jsonify, request, abort
from werkzeug.utils import secure_filename
from src.database_models import *
from src.functions import *


def upload_file():
    """
    Upload csv file containing data to system. Path with description,
    upload data and owner are also stored in database.

    Endpoint: POST /upload_file

    Requires:
    - Authorization header with a valid token
    - MANAGE_FILE permission

    Request Body:
    - Form Data:
        - csv_file: File (CSV file to be uploaded)
        - description: str (Description for the uploaded file)

    Returns:
    - JSON object with text informing of file upload

    Error Responses:
    - 400 Bad Request: If data provided in request body are invalid
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
    - 409 Conflict: If file name provided in request body is already in use
    """
    token = request.headers.get("Authorization")
    status, result = authorize_permissions(token, ["MANAGE_FILE"])

    if status != 200:
        abort(status, description=result)

    print(request.files.keys())
    if "csv_file" not in request.files.keys():
        abort(400, "Missing csv_file in request.")

    if "description" not in request.form.keys():
        abort(400, "Missing description in request.")

    date_uploaded = datetime.utcnow()

    new_file = request.files["csv_file"]
    file_path = os.path.join(
        os.getcwd(), "data_files",
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

    return jsonify("File uploaded successfully")


def get_datasets():
    """
    Retrieves list of datasets.

    Endpoint: GET /get_datasets

    Requires:
    - Authorization header with a valid token
    - MANAGE_FILE permission

    Returns:
    - JSON file with list of datasets

    Error Responses:
    - 403 Forbidden: If user is not logged in or has no permission to access this feature
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

        datasets.append(
            {"file_id": file_id, "file_name": file_name, "desc": file_description, "columns": file_header})

    return jsonify(datasets)