#!/usr/bin/python3
"""
Create a new view for City objects that handles all default RESTFul API
actions.
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()

