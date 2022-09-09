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


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def return_amenities():
    """
    Return amenities - use GET request
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    amenities = storage.all(Amenity)

    # Se crea una lista para guardar los valores que retorna el metodo all(),
    # estos valores son los objetos, los pasamos a un diccionario usando el
    # metodo to_dict() tal cual pide la letra y luego lo pasamos a JSON usando
    # el metodo jsonify
    amenities_list = []
    for key, value in amenities.items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def return_amenities_id(amenity_id):
    """
    Return amenity objects by id or 404 if the id does not exists
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    amenities = storage.all(Amenity)

    # Se hace lo mismo que en la ruta de states pero con la condicion de si se
    # tiene la misma ID que la que se pasa como argumento, si son la misma ID
    # se retorna el valor como diccionario ya que JSON lo entiende.

    for key, value in amenities.items():
        # Condicion para ver si es la misma ID
        if amenities[key].id == amenity_id:
            return value.to_dict()
    # Se usa el metodo abort de flask en caso que no se encuentre la ID pasada
    abort(404)
