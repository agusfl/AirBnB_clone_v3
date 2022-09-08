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
    """
    # Traemos todos los objetos de la clase State que esten en la base de datos
    states = storage.all(State)

    # Se hace lo mismo que en la ruta de states pero con la condicion de si se
    # tiene la misma ID que la que se pasa como argumento, si son la misma ID
    # entonces se hace el append y se retorna esa lista en formato JSON
    states_list = []
    for key, value in states.items():
        # Condicion para ver si es la misma ID
        if states[key].id == state_id:
            states_list.append(value.to_dict())
    return jsonify(states_list)
