#!/usr/bin/python3
"""A module that returns the status of our api"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

ALL = '0.0.0.0'
# GOOGLE = 'https://www.google.com'
ORIGINS = (ALL,)
RESOURCES_PATH = r'/api/v1/*'
RESOURCES = {RESOURCES_PATH: {'origins': ORIGINS}}
CORS(app, resources=RESOURCES)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the storage in case of error"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """A custom 404 error message"""
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
