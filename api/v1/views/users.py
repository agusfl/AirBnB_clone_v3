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
    # Se trae el objeto del User que se pase la "id"
    user = storage.get(User, user_id)

    # If the user_id is not linked to any User object, raise a 404 error
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


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def post_user():
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

    # If the HTTP body request is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
    # traemos con la request en "body"
    obj = User(**body)

    # Si el body no tiene la variable "email" se imprime el error y su status
    if "email" not in body:
        return jsonify('Missing email'), 400
    # Si el body no tiene la variable "password" se imprime el error y su stat
    if "password" not in body:
        return jsonify('Missing password'), 400
    # Si se paso "email" y "pass" se crea el objeto y se guarda en el storage
    else:
        storage.new(obj)
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 201
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_users_id(user_id):
    """
    Make a POST request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP body request is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se trae el objeto del User que se pase la "id"
    user = storage.get(User, user_id)

    # If the user_id is not linked to any User object, raise a 404 error
    if user is None:
        # Se usa el metodo abort de flask en caso que no se pase una ID
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "email", "created_at", "updated_at"]

        for key, value in body.items():
            if key not in keys_ignore:
                setattr(user, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(user.to_dict()), 200)
