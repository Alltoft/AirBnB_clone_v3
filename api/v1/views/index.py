#!/usr/bin/python3
"""Its time to start your API!"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def Json_status():
    """return status route"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'])
def number_obj():
    """return numb of each obj"""
    return (jsonify({"amenity": storage.count("Amenity"),
                     "cities": storage.count("City"),
                     "places": storage.count("Place"),
                     "reviews": storage.count("Review"),
                     "states": storage.count("State"),
                     "users": storage.count("User")}))
