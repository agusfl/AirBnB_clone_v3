#!/usr/bin/python3
"""
Requirements:

- import app_views from api.v1.views
- create a route /status on the object app_views that returns a JSON:
"status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data


@app_views.route("/status", methods=['GET'])
def return_status():
    """Return status of GET request"""
    return jsonify({'status': 'OK'})
