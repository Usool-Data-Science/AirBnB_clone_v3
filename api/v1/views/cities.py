#!/usr/bin/python3
"""A endpoint for cities api"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_state_city(state_id):
    """Retrieve the cities of a particular state"""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)

    cities = [city.to_dict() for city in state.cities]
    response = jsonify(cities)

    return response


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """Returns a specific city based on city_id"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)

    response = jsonify(city.to_dict())

    return response


@app_views.route("/cities/city_id", strict_slashes=False)
def delete_city(city_id):
    """Remove a city from the database based on its id"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("states/<state_id>/cities", methods=["POST"],
                strict_slashes=False)
def add_city(state_id):
    if (request.content_type != 'application/json'):
        return abort(400, "Not a JSON")

    payload = request.get_json()
    if not payload:
        return abort(404, "Not a JSON")

    if 'name' not in payload:
        return abort(400, "Missing name")

    state = storage.get(State, state_id)
    if not state:
        return abort(404)

    payload["state_id"] = state_id
    city = City(**payload)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/city_id", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Modify the existing value of a city"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")

    city = storage.get(City, city_id)
    if city:
        payload = request.get_json()
        if not payload:
            return abort(404, "Not a JSON")

        default_attrs = ['id', 'state_id', 'created_at', 'updated_at']

        for k, v in payload.items():
            if k not in default_attrs:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
