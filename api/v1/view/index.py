#!/usr/bin/python3
"""
Index file for flask app
"""

from models import storage
from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Route - status
    :return: status response json format
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    GET api for status
    :return: respose in json format
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
