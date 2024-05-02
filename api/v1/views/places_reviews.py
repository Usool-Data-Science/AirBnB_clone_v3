#!/usr/bin/python3
"""An endpoint for handling amenities requests"""
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from models.place import Place
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_place_reviews(place_id):
    """Return the full list of reviews in a place"""
    places = storage.get(Place, place_id)

    if places:
        reviews = [review.to_dict() for review in places.reviews]
        response = jsonify(reviews)
        return response
    else:
        return abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_specific_review(review_id):
    """Returns a specific review based on the given id"""
    review = storage.get(Review, review_id)

    if review:
        return jsonify(review.to_dict())
    else:
        return abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a particular review based on its Id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new instance of review"""
    place = storage.get(Place, place_id)
    if place:
        if request.content_type != "application/json":
            return abort(400, "Not a JSON")

        payload = request.get_json()
        if not payload:
            return abort(400, "Not a JSON")

        if "user_id" not in payload:
            return abort(400, "Missing user_id")

        if "text" not in payload:
            return abort(400, "Missing text")

        user_id = payload.get("user_id")

        users = storage.get(User, user_id)
        if not users:
            return abort(404)

        review = Review(**payload)
        review.save()

        return jsonify(review.to_dict()), 201
    else:
        return abort(404)

@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates the name of a specific review"""
    if request.content_type != "application/json":
        return abort(400, "Not a JSON")
    payload = request.get_json()
    if not payload:
        return abort(400, "Not a JSON")

    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'update_at']

    for k, v in payload.items():
        if k not in ignore_keys:
            setattr(review, k, v)

    review.save()
    response = jsonify(review.to_dict())

    return response, 200
