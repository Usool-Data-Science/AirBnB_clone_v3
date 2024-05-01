#!/usr/bin/python3
"""An index to be returned when the api.v1.views is hit"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """The current status of my api"""
    response = {"status": "OK"}
    return jsonify(response)
