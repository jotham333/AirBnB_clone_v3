from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from flasgger.utils import swag_from

def get_user_by_id(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return user

@app_views.route('/users', methods=['GET'])
@swag_from('users_get.yml')
def get_users():
    """ Get all users """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'])
@swag_from('users_get_id.yml')
def get_user(user_id):
    """ Get a user by ID """
    user = get_user_by_id(user_id)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'])
@swag_from('users_delete_id.yml')
def delete_user(user_id):
    """ Delete a user by ID """
    user = get_user_by_id(user_id)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/users', methods=['POST'])
@swag_from('users_post.yml')
def post_user():
    """ Create a user """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'])
@swag_from('users_put_id.yml')
def put_user(user_id):
    """ Update a user by ID """
    user = get_user_by_id(user_id)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
