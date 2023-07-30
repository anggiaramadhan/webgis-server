from flask import jsonify, Response
from shapely.geometry import shape
import geopandas as gpd
import io


def gdf_to_wms_response(gdf):
    gdf["geometry"] = gdf["geometry"].apply(lambda x: shape(x).__geo_interface__)
    features = gdf.to_dict("records")
    response = jsonify(type="FeatureCollection", features=features)
    return response


def gdf_to_geojson(gdf):
    features = []
    for index, row in gdf.iterrows():
        feature = {
            "type": "Feature",
            "geometry": row.geometry.__geo_interface__,
            "properties": row.drop("geometry").to_dict(),
        }
        features.append(feature)
    return features


def gdf_to_wfs_response(gdf):
    output = gdf.to_xml()
    response = Response(output, content_type="application/xml")
    return response


def process_shapefile(file_content):
    gdf = gpd.read_file(io.BytesIO(file_content))
    return gdf.to_json()
