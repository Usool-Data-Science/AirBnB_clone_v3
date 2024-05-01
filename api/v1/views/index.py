#!/usr/bin/python3
"""An index to be returned when the api.v1.views is hit"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def api_status():
    """The current status of my api"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats')
def api_stats():
    """Retrieves the number of each objects by type"""
    response = {"amenities": storage.count('Amenity'),
                "cities": storage.count('City'),
                "places": storage.count('Place'),
                "reviews": storage.count('Review'),
                "states": storage.count('State'),
                "users": storage.count('User')}

    return jsonify(response)
