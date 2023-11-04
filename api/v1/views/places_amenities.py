#!/usr/bin/python3
""" Module of Amenity views """

""" Objects that handle all default RESTful API actions for Place - Amenity """
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

def get_place(place_id):
    """ Retrieve a Place object by its ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return place

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """ Get all amenities for a place """
    place = get_place(place_id)
    return jsonify([amenity.to_dict() for amenity in place.amenities])

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Delete an amenity from a place """
    place = get_place(place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ Add an amenity to a place """
    place = get_place(place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
