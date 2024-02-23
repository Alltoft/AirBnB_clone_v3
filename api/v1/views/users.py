#!/usr/bin/python3
"""a new view for User objects that handles all default RESTFul
API actions"""
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users_list = [u.to_dict() for u in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def id_User(user_id):
    """Retrieves a User object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(user_id):
    """Deletes a User object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post():
    """Creates a User"""
    dict = request.get_json(silent=True)
    if dict is None:
        abort(400, 'Not a JSON')
    if dict.get("email") is None:
        abort(400, 'Missing email')
    if dict.get("password") is None:
        abort(400, 'Missing password')
    new_status = User(**dict)
    new_status.save()
    return jsonify(new_status.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put(user_id):
    """Updates a User object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    dict = request.get_json(silent=True)
    if dict is None:
        abort(400, 'Not a JSON')
    keys_substract = ['id', 'created_at', 'updated_at']
    for key, val in dict.items():
        if key not in keys_substract:
            setattr(users, key, val)
    storage.save()
    return jsonify(users.to_dict()), 200
