from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import geopandas as gpd
import os
import json
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URI"]
db = SQLAlchemy(app)

from models import GeoData
from helpers import gdf_to_wfs_response


@app.route("/files")
def uploaded_files():
    files = GeoData.query.all()
    file_list = [{"id": file.id, "name": file.name} for file in files]
    return jsonify(file_list)


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = file.filename
    file_content = file.read()
    data = json.loads(file_content)

    geo_data = GeoData(name=filename, data=json.dumps(data))
    db.session.add(geo_data)
    db.session.commit()

    return "file have been uploaded"


@app.route("/wfs/<int:id>")
def serve_wfs(id):
    geo_data = GeoData.query.get(id)
    if not geo_data:
        return "geodata not found"

    gdf = gpd.read_file(io.StringIO(geo_data.data))
    return gdf_to_wfs_response(gdf)
