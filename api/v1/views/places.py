#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default HTTP methods.
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def return_places(city_id):
    """
    Return places - use GET request.
    Cada lugar (places) esta directamente relacionado con la ciudad, no puede
    haber lugares sin ciudades.
    """
    # Traemos el objeto especifico de city por id con el metódo get
    # creado en DBStorage
    city = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if city is None:
        # Se usa el metodo abort de flask en caso que no se encuentre la ID
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def return_places_id(place_id):
    """
    Return place objects by id or 404 if the id does not exists.
    """
    # Traemos el objeto especifico de place por id con el metódo get
    # creado en DBStorage.
    place = storage.get(Place, place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places_id(place_id):
    """
    Delete a Place object by id.
    """
    # Se trae el objeto Place que se pase la "id"
    place = storage.get(Place, place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place is None:
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(place)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places/", strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """
    Create a Place object.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Traemos City object por su "id"
    city = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if city is None:
        abort(404)

    # Si el body no tiene la variable "user_id" se imprime el error y su stat
    if "user_id" not in body:
        return (jsonify({'error': 'Missing user_id'}), 400)

    # Usamos el metodo get() de python para obtener el user_id
    user_id = body.get("user_id")
    # creamos un usuario usando el metodo get() que creamos nosotros
    user = storage.get(User, user_id)
    # If the user_id is not linked to any User object, raise a 404 error
    if user is None:
        abort(404)

    # Si el body no tiene la variable "name" se imprime el error y su status
    if "name" not in body:
        return (jsonify({'error': 'Missing name'}), 400)

    # Si se paso "name" se crea el objeto y se guarda en la base de datos
    # Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
    # traemos con la request en "body"
    # Se agrega las "id" al dic "body", ya que en el body de la request
    # solo se mandan los datos de json no esta la id de state_id en el body
    body['city_id'] = city_id
    body['user_id'] = user_id

    # Se crea una instancia de la clase Place
    obj = Place(**body)

    storage.new(obj)
    # Se guarda el nuevo objeto dentro del storage
    storage.save()

    # Se devuelve el objeto creado y un status code de 201
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_places_id(place_id):
    """
    Make a PUT request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se trae el objeto del place que se pase la "id"
    place = storage.get(Place, place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place is None:
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]

        for key, value in body.items():
            if key not in keys_ignore:
                setattr(place, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(place.to_dict()), 200)
