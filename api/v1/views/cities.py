#!/usr/bin/python3
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from flasgger.utils import swag_from
from models.state import State

# Helper function for retrieving a city by ID
def get_city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@swag_from('cities_get.yml')
def get_cities(state_id):
    """ Get all cities in a state """
    cities = [city.to_dict() for city in storage.all(City).values() if city.state_id == state_id]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('cities_get_id.yml')
def get_city(city_id):
    """ Get a city by id """
    city = get_city_by_id(city_id)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('cities_delete_id.yml')
def delete_city(city_id):
    """ Delete a city by id """
    city = get_city_by_id(city_id)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('cities_post.yml')
def post_city(state_id):
    """ Create a new city in a state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    data['state_id'] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('cities_put_id.yml')
def put_city(city_id):
    """ Update a city by id """
    city = get_city_by_id(city_id)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
