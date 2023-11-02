#!/usr/bin/python3
""" Place Module for HBNB project """

from models.city import City
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from flasgger.utils import swag_from

def get_place_by_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return place

@app_views.route('cities/<city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('places_get.yml')
def get_places(city_id):
    """ Get all places in a city """
    places = [place.to_dict() for place in storage.all(Place).values() if place.city_id == city_id]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('places_get_id.yml')
def get_place(place_id):
    """ Get a place by ID """
    place = get_place_by_id(place_id)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('places_delete_id.yml')
def delete_place(place_id):
    """ Delete a place by ID """
    place = get_place_by_id(place_id)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
@swag_from('places_post.yml')
def post_place(city_id):
    """ Create a new place in a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('places_put_id.yml')
def put_place(place_id):
    """ Update a place by ID """
    place = get_place_by_id(place_id)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

@app_views.route('/api/v1/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    # Get the JSON data from the request body
    data = request.get_json()

    # Validate the JSON data
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400

    # Extract the optional keys from the JSON data
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Retrieve all Place objects
    if not states and not cities and not amenities:
        places = storage.all().values()
    else:
        places = []

        # Filter by states
        if states:
            for state_id in states:
                for city in storage.all().values():
                    if state_id == city.state_id:
                        places.append(city)

        # Filter by cities
        if cities:
            for city_id in cities:
                for city in storage.all().values():
                    if city_id == city.id:
                        places.append(city)

        # Filter by amenities
        if amenities:
            for amenity_id in amenities:
                for place in storage.all().values():
                    if amenity_id in place.amenity_ids:
                        places.append(place)

    # Return the filtered places
    return jsonify([place.to_dict() for place in places]), 200
