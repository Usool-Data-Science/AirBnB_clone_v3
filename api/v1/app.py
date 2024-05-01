#!/usr/bin/python3
"""A module that returns the status of our api"""
from os import getenv
from flask import Flask
from models import storage
from api.vi.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def closing():
    """
        A method that calls that closes the database
        or fileStorage
    """
    return storage.close()


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', 5000)
    app.run(hosts=HOST, port=PORT, threaded=True)
