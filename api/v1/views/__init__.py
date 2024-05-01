#!/usr/bin/python3
"""A initialization that declares the flask Blueprint"""
from flask import Blueprint

app_view = Blueprint("app_views", __name__, url_prefix='/api/vi')

from api.vi.views.index import *
