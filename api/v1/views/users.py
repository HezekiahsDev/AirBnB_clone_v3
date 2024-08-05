#!/usr/bin/python3
""" Handles all default RESTful API actions for User objects """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_all_users():
    """
    Retrieves a list of all User objects.
    """
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a single User object by its ID.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object by its ID.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def create_user():
    """
    Creates a new User object.
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user(user_id):
    """
    Updates an existing User object by its ID.
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    ignored_keys = ['id', 'email', 'created_at', 'updated_at']

    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    data = request.get_json()
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
