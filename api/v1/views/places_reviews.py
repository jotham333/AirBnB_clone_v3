from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from flasgger.utils import swag_from

def get_review_by_id(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return review

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@swag_from('reviews_get.yml')
def get_reviews(place_id):
    """ Get reviews for a specific place by place_id """
    reviews = [review.to_dict() for review in storage.all(Review).values() if review.place_id == place_id]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'])
@swag_from('reviews_get_id.yml')
def get_review(review_id):
    """ Get a review by ID """
    review = get_review_by_id(review_id)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
@swag_from('reviews_delete_id.yml')
def delete_review(review_id):
    """ Delete a review by ID """
    review = get_review_by_id(review_id)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
@swag_from('reviews_post.yml')
def post_review(place_id):
    """ Create a new review for a place """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT'])
@swag_from('reviews_put_id.yml')
def put_review(review_id):
    """ Update a review by ID """
    review = get_review_by_id(review_id)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
