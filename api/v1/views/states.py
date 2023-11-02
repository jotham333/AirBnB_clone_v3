#!/usr/bin/python3
""" State Module for HBNB project """

from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from flasgger.utils import swag_from

# Helper function to retrieve a state by ID
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return state

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('states_get.yml')
def get_states():
    """ Get all states """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('states_get_id.yml')
def get_state(state_id):
    """ Get a state by ID """
    state = get_state_by_id(state_id)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('states_delete_id.yml')
def delete_state(state_id):
    """ Delete a state by ID """
    state = get_state_by_id(state_id)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('states_post.yml')
def post_state():
    """ Create a state """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('states_put_id.yml')
def put_state(state_id):
    """ Update a state by ID """
    state = get_state_by_id(state_id)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
