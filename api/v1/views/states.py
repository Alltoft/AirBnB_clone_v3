#!/usr/bin/python3
"""a new view for State objects that handles all default RESTFul
API actions"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = [s.to_dict() for s in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def id_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """Creates a State"""
    dict = request.get_json()
    if dict is None:
        abort(400, 'Not a JSON')
    if dict.get("name") is None:
        abort(400, 'Missing name')
    new_status = State(**dict)
    new_status.save()
    return jsonify(new_status.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing state object based on id
           Parameters:
               state_id [str]: the id of the state to update

           Returns:
               A JSON dictionary of the udpated state in a 200 response
               A 400 response if not a valid JSON
               A 404 response if the id does not match
    """
    state = storage.get('State', state_id)
    error_message = ""
    if state:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(state, name, value)
            storage.save()
            return jsonify(state.to_dict())
        else:
            error_message = "Not a JSON"
            response = jsonify({'error': error_message})
            response.status_code = 400
            return response

    abort(404)
