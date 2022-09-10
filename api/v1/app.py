#!/usr/bin/python3
"""
First endpoint (route) will be to return the status of your API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv  # for environmental variables
from flask import make_response  # for task 6 - errorhandler(404)
from flask import jsonify  # convert to JSON data
from flask_cors import CORS

# Creando una instancia de flask con el nombre del archivo nuestro
app = Flask(__name__)
# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)
# Allow CORS (Cross origin resource shearing)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(self):
    """
    After each request you must remove the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Use of decorator for error handler -> 404 (page not found)
    Can`t use HTML, CSS you need to return JSON format.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    """
    Set host IP addres and port
    Set option threaded=True for handling requests concurrently
    getenv() --> https://www.geeksforgeeks.org/python-os-getenv-method/
    """
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
