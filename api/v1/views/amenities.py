#!/usr/bin/python3

from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from flasgger.utils import swag_from


def get_amenity_by_id(amenity_id):
    """ Helper function to retrieve an amenity by ID """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('amenities_get.yml')
def get_amenities():
    """ Get all amenities """
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
@swag_from('amenities_get_id.yml')
def get_amenity(amenity_id):
    """ Get an amenity by ID """
    amenity = get_amenity_by_id(amenity_id)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('amenities_delete_id.yml')
def delete_amenity(amenity_id):
    """ Delete an amenity by ID """
    amenity = get_amenity_by_id(amenity_id)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('amenities_post.yml')
def post_amenity():
    """ Create an amenity """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('amenities_put_id.yml')
def put_amenity(amenity_id):
    """ Update an amenity by ID """
    amenity = get_amenity_by_id(amenity_id)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
