#!/usr/bin/python3
"""
First endpoint (route) will be to return the status of your API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv  # for environmental variables

# Creando una instancia de flask con el nombre del archivo nuestro
app = Flask(__name__)
# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """
    After each request you must remove the current SQLAlchemy Session
    """
    storage.close()


if __name__ == '__main__':
    """
    Set host IP addres and port
    Set option threaded=True for handling requests concurrently
    """
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
