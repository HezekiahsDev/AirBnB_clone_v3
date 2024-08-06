#!/usr/bin/python3
"""
Module for Review routes
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    :param place_id: Place ID
    :return: list of Review objects in JSON format
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews  # Accessing related reviews
    review_list = [review.to_dict() for review in reviews]
    return make_response(jsonify(review_list), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object by ID
    :param review_id: Review ID
    :return: Review object in JSON format
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object by ID
    :param review_id: Review ID
    :return: empty dictionary with status code 200
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a Review for a Place
    :param place_id: Place ID
    :return: new Review object in JSON format
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, review_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in review_data:
        abort(400, 'Missing text')

    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object by ID
    :param review_id: Review ID
    :return: updated Review object in JSON format
    """
    Ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, 'Not a JSON')
    for key, value in review_data.items():
        if key not in Ignore_keys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
