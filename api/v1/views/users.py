#!/usr/bin/python3
"""An endpoint for handling amenities requests"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False)
def get_users():
    """Return the full list of end users in a state"""
    users = []
    for k, v in storage.all(User).items():
        amenities.append(v.to_dict())
    response = jsonify(users)

    return response


@app_views.route("/users/<user_id>", strict_slashes=False)
def get_specific_user(user_id):
    """Returns a specific user based on the given id"""
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a particular user based on its Id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a new instance of user"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")

    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    if "email" not in payload:
        return abort(400, "Missing email")

    if "password" not in payload:
        return abort(400, "Missing password")

    user = User(**payload)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates the name of a specific amenity"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")
    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    user = storage.get(User, user_id)
    ignore_keys = ['id', 'email', 'created_at', 'update_at']

    for k, v in payload.items():
        if k not in ignore_keys:
            setattr(user, k, v)

    user.save()
    response = jsonify(user.to_dict())

    return response, 200
