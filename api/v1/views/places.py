#!/usr/bin/python3
"""An endpoint for handling amenities requests"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.amenity import Amenity
from models.state import State
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
            return abort(404)

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


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def search_places():
    """Return the lisf of places based on some filter criteria"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")

    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    state_filter = payload.get('states')
    city_filter = payload.get('cities')
    amenity_filter = payload.get('amenities')

    # Return all places if no filter is given
    if not (state_filter or city_filter or amenity_filter):
        places = storage.all(Place).values()
        all_places = [place.to_dict() for place in places]
        response = jsonify(all_places)

        return response

    # If atleast one filter is given, append the places in it to a set
    all_places = set()

    if state_filter:
        state_objs = [storage.get(State, st_id) for st_id in state_filter]
        for state in state_objs:
            if state:
                for city in state.city:
                    if city:
                        for place in city.places:
                            all_places.update(place)

    if city_filter:
        city_objs = [storage.get(City, city_id) for city_id in city_filter]

        for city in city_objs:
            if city:
                for place in city.place:
                    all_places.update(place)

    """
    Use the amenities provide to filter all places only when there
    is no places retrieved using the city-states and also when
    the amenities filter are provided simulataneously. Otherwise
    we won't retrieve anything.
    """
    if amenity_filter and not all_places:
        places = storage.all(Place).values()
        amn_objs = [storage.get(Amenity, amn_id) for amn_id in amenity_filter]
        for place in places:
            if all(amn in place.amenities for amn in amn_objs):
                all_places.update(place)

    # Convert the places to dict and remove the list of amenities from it.
    final_places = []
    for place in all_places:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        final_places.append(place_dict)
    response = jsonify(final_places)

    return response
