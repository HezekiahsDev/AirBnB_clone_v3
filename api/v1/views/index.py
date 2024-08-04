#!/usr/bin/python3
"""
Flask index file
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    router for status api GET method
    :return: status response in JSON format
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
    stats - returns the stats (info) of a class
    :return: class information in JSON format
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
