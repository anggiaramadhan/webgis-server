from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import geopandas as gpd
import zipfile
import os
import json
import io

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://localhost:5173"])
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URI"]
db = SQLAlchemy(app)

from models import GeoData
from helpers import process_shapefile, gdf_to_geojson


@app.route("/files")
def uploaded_files():
    files = GeoData.query.all()
    file_list = [{"id": file.id, "name": file.name} for file in files]
    return jsonify(file_list)


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = file.filename
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    if filename.endswith(".json"):
        with open(filepath, 'r') as file:
            file_content = file.read()
            data = json.loads(file_content)
            geojson = json.dumps(data)
    elif filename.endswith(".zip"):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall('uploads')

            shapefile_name = None
            for extracted_file in os.listdir('uploads'):
                if extracted_file.endswith('.shp'):
                    shapefile_name = os.path.join('uploads', extracted_file)
                    break

            if shapefile_name is not None:
                data = gpd.read_file(shapefile_name)
                geojson = data.to_json()
    else:
        return "Unsupported file format. Only GeoJSON and Shapefile (SHP) are allowed."

    geo_data = GeoData(name=filename, data=geojson)
    db.session.add(geo_data)
    db.session.commit()

    return jsonify({"message": "File upload successful", "data": json.loads(geojson)}), 200


@app.route("/wfs/<int:id>")
def serve_wfs(id):
    geo_data = GeoData.query.get(id)
    if not geo_data:
        return "geodata not found"

    gdf = gpd.read_file(io.StringIO(geo_data.data))
    features = gdf_to_geojson(gdf)
    return jsonify({"type": "FeatureCollection", "features": features})
