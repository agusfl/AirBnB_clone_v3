#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default RESTFul API
actions.
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models.city import City
from models.place import Place
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def return_places(city_id):
    """
    Return places - use GET request
    Cada lugar (places) esta directamente relacionado con la ciudad, no puede
    haber lugares sin ciudades.
    """
    # Traemos el objeto especifico de city por id con el metódo get
    # creado en DBStorage
    city = storage.get(City, city_id)

    # Si city llega vacío
    if city is None:
        # Se usa el metodo abort de flask en caso que no se encuentre la ID
        abort(404)
    places = []
    for place in city.cities:
        cities.append(place.to_dict())
    return jsonify(cities)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def return_places_id(place_id):
    """
    Return state objects by id or 404 if the id does not exists
    """
    # Traemos el objeto especifico de place por id con el metódo get
    # Creado en DBStorage
    place = storage.get(Place, place_id)

    # Si place llega vacío
    if place is None:
        # Se usa el metodo abort de flask en caso que no se encuentre la ID
        abort(404)
    # de lo contrario devolvemos el objeto pasado a json:
    return jsonify(place.to_dict())
