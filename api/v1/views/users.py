#!/usr/bin/python3
"""
Create a new view for State objects that handles all default RESTFul API
actions.
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models.user import User
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def return_users():
    """
    Return users - use GET request
    """
    # Traemos todos los objetos de la clase User que esten en la base de datos
    users = storage.all(User)

    # Se crea una lista para guardar los valores que retorna el metodo all(),
    # estos valores son los objetos, los pasamos a un diccionario usando el
    # metodo to_dict() tal cual pide la letra y luego lo pasamos a JSON usando
    # el metodo jsonify
    users_list = []
    for key, value in users.items():
        users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def return_users_id(user_id):
    """
    Return amenity objects by id or 404 if the id does not exists
    """
    # Traemos todos los objetos de la clase User que esten en la base de datos
    users = storage.all(User)

    # Se hace lo mismo que en la ruta de users pero con la condicion de si se
    # tiene la misma ID que la que se pasa como argumento, si son la misma ID
    # se retorna el valor como diccionario ya que JSON lo entiende.

    for key, value in users.items():
        # Condicion para ver si es la misma ID
        if users[key].id == user_id:
            return value.to_dict()
    # Se usa el metodo abort de flask en caso que no se encuentre la ID pasada
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users_id(user_id):
    """
    If the user_id is not linked to any User object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    # Traemos todos los objetos de la clase User que esten en la base de datos
    user = storage.get(User, user_id)

    if user is None:
        # Se usa el metodo abort de flask en caso que no se pase una ID
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(user)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)
