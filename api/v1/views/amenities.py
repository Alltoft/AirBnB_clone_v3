#!/usr/bin/python3
"""creation of a new view for amenity that handles all api actions"""
from models.amenity import Amenity
from flask import Flask, jsonify, Blueprint, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """gets info about all amenity objetcts from storage"""
    all_amenities = storage.all(Amenity).values()
    dict_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(dict_amenities)

@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """gets info about amenity objects based on their id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity, and if"""
    """and if amenity_id is not linked to any Amenity object, raise 404"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """posting a new amenity"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_data:
        abort(400, 'Missing name')
    amenity = Amenity(**amenity_data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, 'Not a JSON')
    excluded_keys = ['id', 'created_at', 'updated_at']
    for key, val in amenity_data.items():
        if key not in excluded_keys:
            setattr(amenity, key, val)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
