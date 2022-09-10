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
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def return_cities(state_id):
    """
    Return cities - use GET request
    No es necesario poner la opcion methods aca ya que GET se hace por default,
    lo ponemos por mayor claridad nomas.
    Se pone la opcion de strict_slashes=False para que no haya problemas si se
    pasa un / (slash) al final de la ruta y que corra igual.
    """
    # Traemos el objeto especifico de state por id con el metódo get
    # Creado en DBStorage
    states = storage.get(State, state_id)

    # If the state_id is not linked to any State object, raise a 404 error
    if states is None:
        abort(404)

    cities = []
    for city in states.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def return_cities_id(city_id):
    """
    Return state objects by id or 404 if the id does not exists
    Info abort --> https://flask-restplus.readthedocs.io/en/stable/errors.html
    """
    # Traemos el objeto especifico de city por id con el metódo get
    # Creado en DBStorage
    cities = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if cities is None:
        abort(404)
    # Se devuelve el objeto pasado a json:
    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities_id(city_id):
    """
    If the city_id is not linked to any State object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    # Se trae el objeto City del cual se pase la "id"
    city = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if city is None:
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(city)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities/", strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
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

    # If the HTTP body request is not a valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Traemos state por su "id"
    state = storage.get(State, state_id)

    # If the state_id is not linked to any State object, raise a 404 error
    if state is None:
        abort(404)

    # Si el body no tiene la variable "name" se imprime el error y su stat
    if "name" not in body:
        return (jsonify({'error': 'Missing name'}), 400)

    # Si se paso "name" se crea el objeto y se guarda en la base de datos
    # Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
    # traemos con la request en "body"
    # Se agrega el state_id al dic "body", ya que en el body de la request
    # solo se mandan los datos de json no esta la id de state_id en el body
    body['state_id'] = state_id
    obj = City(**body)

    storage.new(obj)
    # Se guarda el nuevo objeto dentro del storage
    storage.save()

    # Se devuelve el objeto creado y un status code de 201
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_cities_id(city_id):
    """
    Make a POST request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se trae el objeto de la ciudad que se pase la "id"
    city = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if city is None:
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "state_id", "created_at", "updated_at"]

        for key, value in body.items():
            if key not in keys_ignore:
                setattr(city, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(city.to_dict()), 200)
