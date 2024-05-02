#!/usr/bin/python3
"""An endpoint for handling amenities requests"""
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.state import State
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """Return the full list of available amenities in a state"""
    amenities = []
    for k, v in storage.all(Amenity).items():
        amenities.append(v.to_dict())
    response = jsonify(amenities)

    return response


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_specific_amenities(amenity_id):
    """Returns a specific amenity based on the given id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a particular amenity based on its Id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new instance of amenity"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")

    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    if "name" not in payload:
        return abort(400, "Missing name")

    amenity = Amenity(**payload)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the name of a specific amenity"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")
    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    amenity = storage.get(Amenity, amenity_id)
    ignore_keys = ['id', 'created_at', 'update_at']

    for k, v in payload.items():
        if k not in ignore_keys:
            setattr(amenity, k, v)

    amenity.save()
    response = jsonify(amenity.to_dict())

    return response, 200
