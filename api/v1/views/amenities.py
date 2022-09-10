#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default RESTFul API
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
    # Traemos todos los objetos de la clase Amenity que esten en el storage
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
    # Traemos todos los objetos de la clase Amenity que esten en el storage
    amenities = storage.all(Amenity)

    # Se hace lo mismo que en la ruta de amenities pero con la condicion de si
    # tiene la misma ID que la que se pasa como argumento, si son la misma ID
    # se retorna el valor como diccionario ya que JSON lo entiende.

    for key, value in amenities.items():
        # Condicion para ver si es la misma ID
        if amenities[key].id == amenity_id:
            return value.to_dict()
    # Se usa el metodo abort de flask en caso que no se encuentre la ID pasada
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities_id(amenity_id):
    """
    If the amenity_id is not linked to any Amenity object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    # Se trae el objeto Amenity del cual se pase la "id"
    amenity = storage.get(Amenity, amenity_id)

    # If the amenity_id is not linked to any Amenity object, raise a 404 error
    if amenity is None:
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(amenity)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def post_amenity():
    """
    - You must use request.get_json from Flask to transform the HTTP body
    request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400 error with the
    message Not a JSON
    - If the dictionary doesn’t contain the key name, raise a 400 error with
    the message Missing name
    - Returns the new State with the status code 201
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
    # traemos con la request en "body"
    obj = Amenity(**body)

    # Si el body no tiene la variable "name" se imprime el error y su stat
    if "name" not in body:
        return jsonify('Missing name'), 400
    # Si se paso "name" se crea el objeto y se guarda en la base de datos
    else:
        storage.new(obj)
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 201
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities_id(amenity_id):
    """
    Make a POST request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se trae el objeto Amenity del cual se pase la "id"
    amenity = storage.get(Amenity, amenity_id)

    # If the amenity_id is not linked to any Amenity object, raise a 404 error
    if amenity is None:
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "created_at", "updated_at"]

        for key, value in body.items():
            if key not in keys_ignore:
                setattr(amenity, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(amenity.to_dict()), 200)
