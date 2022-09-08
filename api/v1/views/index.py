#!/usr/bin/python3
"""
Requirements:

- import app_views from api.v1.views
- create a route /status on the object app_views that returns a JSON:
"status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models import Amenity, City, Place, Review, State, User


@app_views.route("/status", methods=['GET'])
def return_status():
    """Return status of GET request"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=['GET'])
def return_stats():
    """Return the number of each object by type"""
    return jsonify({'amenities': storage.count(Amenity),
                    'cities': storage.count(City),
                    'places': storage.count(Place),
                    'reviews': storage.count(Review),
                    'states': storage.count(State),
                    'users': storage.count(User)})
