#!/usr/bin/python3
"""a new view for State objects that handles all default RESTFul
API actions"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all State objects"""
    amenities = storage.all(Amenity).values()
    amenities_list = [a.to_dict() for a in amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def id_amenity(amenity_id):
    """Retrieves a State object"""
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(amenity_id):
    """Deletes a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post():
    """Creates a State"""
    dict = request.get_json(silent=True)
    if dict is None:
        abort(400, 'Not a JSON')
    if dict.get("name") is None:
        abort(400, 'Missing name')
    new_status = Amenity(**dict)
    new_status.save()
    return jsonify(new_status.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put(amenity_id):
    """Updates a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    dict = request.get_json(silent=True)
    if dict is None:
        abort(400, 'Not a JSON')
    keys_substract = ['id', 'created_at', 'updated_at']
    for key, val in dict.items():
        if key not in keys_substract:
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
