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


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places_id(place_id):
    """
    If the place_id is not linked to any City object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    place = storage.get(Place, place_id)

    if place is None:
        # Se usa el metodo abort de flask en caso que no se pase una ID
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(place)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)
