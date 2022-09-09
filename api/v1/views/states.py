#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul API
actions.
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models.state import State
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def return_states():
    """
    Return states - use GET request
    No es necesario poner la opcion methods aca ya que GET se hace por default,
    lo ponemos por mayor claridad nomas.
    Se pone la opcion de strict_slashes=False para que no haya problemas si se
    pasa un / (slash) al final de la ruta y que corra igual.
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    states = storage.all(State)

    # Se crea una lista para guardar los valores que retorna el metodo all(),
    # estos valores son los objetos, los pasamos a un diccionario usando el
    # metodo to_dict() tal cual pide la letra y luego lo pasamos a JSON usando
    # el metodo jsonify
    states_list = []
    for key, value in states.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def return_states_id(state_id):
    """
    Return state objects by id or 404 if the id does not exists
    Info abort --> https://flask-restplus.readthedocs.io/en/stable/errors.html
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    states = storage.all(State)

    # Se hace lo mismo que en la ruta de states pero con la condicion de si se
    # tiene la misma ID que la que se pasa como argumento, si son la misma ID
    # se retorna el valor como diccionario ya que JSON lo entiende.

    for key, value in states.items():
        # Condicion para ver si es la misma ID
        if states[key].id == state_id:
            return value.to_dict()
    # Se usa el metodo abort de flask en caso que no se encuentre la ID pasada
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states_id(state_id):
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


@app_views.route("/states", strict_slashes=False, methods=['POST'])
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
    # Hacemos la request de la data que se pase en formato json y la pasamos
    # a un dic de python para poder trabajar con ella
    json = request.get_json()

    # Si no es formato JSON imprimos el mensaje de error correspondiente
    if not json:
        abort(400, 'Not a JSON')
    # Si el json no tiene la variable "name" se imprime el error con su sataus
    elif not json['name']:
        abort(400, 'Missing name')
    # Si se paso "name" se crea el objeto y se guarda en la base de datos
    else:
        storage.new(json)
        storage.save()
        # Se devuelve el objeto creado y un status code de 201
        return make_response(jsonify(json), 201)
