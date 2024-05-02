#!/usr/bin/python3
"""An endpoint for handling amenities requests"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places_in_city(city_id):
    """Return the full list of places in a city"""
    city = storage.get(City, city_id)

    if city:
        places = [place.to_dict() for place in city.places]
        response = jsonify(places)
        return response
    else:
        return abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_specific_place(place_id):
    """Returns a specific place based on the given id"""
    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a particular place based on its Id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new instance of place"""
    city = storage.get(City, city_id)
    if city:
        if request.content_type != "application/json":
            return abort(400, "Not a JSON")

        payload = request.get_json()
        if not payload:
            return abort(400, "Not a JSON")

        if "user_id" not in payload:
            return abort(400, "Missing user_id")

        if "name" not in payload:
            return abort(400, "Missing name")

        user_id = payload.get("user_id")
        
        users = storage.get(User, user_id)
        if not users:
            return abort(404, "NO USER WITH THIS ID")

        place = Place(**payload)
        place.save()

        return jsonify(place.to_dict()), 201
    else:
        return abort(404)

@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Updates the name of a specific amenity"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")
    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'update_at']

    for k, v in payload.items():
        if k not in ignore_keys:
            setattr(place, k, v)

    place.save()
    response = jsonify(place.to_dict())

    return response, 200
