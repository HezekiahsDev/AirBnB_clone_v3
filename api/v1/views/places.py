#!/usr/bin/python3
""" Handles all default RESTful API actions for Place objects """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects within a specific City.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a specific Place object by its ID.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object by its ID.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def create_place(city_id):
    """
    Creates a new Place object within a specified City.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, description="User not found")

    if 'name' not in data:
        abort(400, description="Missing name")

    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def update_place(place_id):
    """
    Updates an existing Place object by its ID.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignored_fields = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignored_fields:
            setattr(place, key, value)
    
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def search_places():
    """
    Retrieves Place objects based on criteria provided in the request body.
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states_ids = data.get('states', [])
    cities
