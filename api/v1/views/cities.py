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


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def return_cities():
    """
    Return cities - use GET request
    No es necesario poner la opcion methods aca ya que GET se hace por default,
    lo ponemos por mayor claridad nomas.
    Se pone la opcion de strict_slashes=False para que no haya problemas si se
    pasa un / (slash) al final de la ruta y que corra igual.
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    states = storage.all(City)

    # Se crea una lista para guardar los valores que retorna el metodo all(),
    # estos valores son los objetos, los pasamos a un diccionario usando el
    # metodo to_dict() tal cual pide la letra y luego lo pasamos a JSON usando
    # el metodo jsonify
    cities = []
    for city in states.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def return_cities_id(city_id):
    """
    Return state objects by id or 404 if the id does not exists
    Info abort --> https://flask-restplus.readthedocs.io/en/stable/errors.html
    """
    # Traemos el objeto especifico de city por id con el metódo get
    # Creado en DBStorage
    cities = storage.get("City", city_id)

    # Si city llega vacío
    if cities is None:
        # Se usa el metodo abort de flask en caso que no se encuentre la ID
        abort(404)
    # de lo contrario devolvemos el objeto pasado a json:
    # 1ero (<dict>) 2do (json)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities_id(city_id):
    """
    If the state_id is not linked to any State object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    state = storage.get(State, state_id)

    if state is None:
        # Se usa el metodo abort de flask en caso que no se pase una ID
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(state)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities/", strict_slashes=False,
                 methods=['POST'])
def post_state():
    """
    - You must use request.get_json from Flask to transform the HTTP body
    request to a dictionary
    - If the HTTP body request is not valid JSON, raise a 400 error with the
    message Not a JSON
    - If the dictionary doesn’t contain the key name, raise a 400 error with
    the message Missing name
    - Returns the new State with the status code 201
    """
    try:
        # Hacemos la request de la data que se pase en formato json y la
        # pasamos a un dic de python para poder trabajar con ella
        json = request.get_json()

        # Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
        # traemos con la request en "json"
        obj = State(**json)

        # Si el json no tiene la variable "name" se imprime el error y su stat
        if "name" not in json:
            return jsonify('Missing name'), 400
        # Si se paso "name" se crea el objeto y se guarda en la base de datos
        else:
            storage.new(obj)
            # Se guarda el nuevo objeto dentro del storage
            storage.save()
            # Se devuelve el objeto creado y un status code de 201
            return make_response(jsonify(obj.to_dict()), 201)
    except Exception as e:
        abort(400, 'Not a JSON')


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_cities_id(state_id):
    """
    Make a POST request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    json = request.get_json()

    if json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Traemos todos los objetos de la clase State que esten en el storage
    state = storage.get(State, state_id)

    if state is None:
        # Se usa el metodo abort de flask en caso que no se pase una ID
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "created_at", "updated_at"]

        for key, value in json.items():
            if key not in keys_ignore:
                setattr(state, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(state.to_dict()), 200)
