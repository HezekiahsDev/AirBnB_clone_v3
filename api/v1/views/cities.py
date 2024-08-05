#!/usr/bin/python3
""" Handles all default RESTful API actions for City objects """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects within a specific State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a specific City object by its ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object by its ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def create_city(state_id):
    """
    Creates a new City object within a specified State.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    
    if not request.is_json:
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    
    new_city = City(**data)
    new_city.state_id = state.id
    new_city.save()
    
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def update_city(city_id):
    """
    Updates an existing City object by its ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    
    if not request.is_json:
        abort(400, description="Not a JSON")
    
    ignored_fields = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()

    for key, value in data.items():
        if key not in ignored_fields:
            setattr(city, key, value)
    
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
