from flask import jsonify, Response
from shapely.geometry import shape


def gdf_to_wms_response(gdf):
    gdf["geometry"] = gdf["geometry"].apply(lambda x: shape(x).__geo_interface__)
    features = gdf.to_dict("records")
    response = jsonify(type="FeatureCollection", features=features)
    return response


def gdf_to_wfs_response(gdf):
    output = gdf.to_xml()
    response = Response(output, content_type="application/xml")
    return response
