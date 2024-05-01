#!/usr/bin/python3
"""An index to be returned when the api.v1.views is hit"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """Returns all states in our database"""
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    response = jsonify(state_list)

    return response


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_specific_state(state_id):
    """Returns a specific state equivalent to state_id"""
    state = storage.get(State, state_id)
    if state:
        response = jsonify(state.to_dict())
        return response
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_specific_state(state_id):
    """Deletes a specific state equivalent to state_id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a specific state equivalent to state_id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')

    state_props = request.get_json()
    if 'name' not in state_props:
        abort(400, 'Missing name')

    state = State(**state_props)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a specific state equivalent to state_id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')

    if not request.get_json():
        return abort(400, 'Not a JSON')
    else:
        state_prop = request.get_json()

    state = storage.get(State, state_id)
    if not state:
        return abort(404)

    to_ignore = ['id', 'created_at', 'updated_at']

    for key, val in state_prop.items():
        if key not in to_ignore:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
