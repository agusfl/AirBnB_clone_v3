#!/usr/bin/python3
"""
Create a new view for Review objects that handles all default RESTFul API
actions.
"""
from api.v1.views import app_views
from flask import jsonify  # convert to JSON data
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort
from flask import make_response  # errorhandler(404)
from flask import request  # for get_json()


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def return_reviews(place_id):
    """
    Return reviews - use GET request
    Cada lugar (places) esta directamente relacionado con las reviews, no puede
    haber reviews no linkeadas con algún lugar.
    """
    # Traemos el objeto especifico de place por id con el metódo get
    # creado en DBStorage
    place = storage.get(Place, place_id)

    # Si place llega vacío
    if place is None:
        # Se usa el metodo abort de flask en caso que no se encuentre la ID
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def return_reviews_id(review_id):
    """
    Return review objects by id or 404 if the id does not exists
    """
    # Traemos el objeto especifico de place por id con el metódo get
    # Creado en DBStorage
    review = storage.get(Review, review_id)

    # Si review llega vacío
    if review is None:
        # Se usa el metodo abort de flask en caso que no se encuentre la ID
        abort(404)
    # de lo contrario devolvemos el objeto pasado a json:
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_id(review_id):
    """
    If the review_id is not linked to any Review object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    # Se trae el objeto Review que se pase la "id"
    review = storage.get(Review, review_id)

    # If the review_id is not linked to any Review object, raise a 404 error
    if review is None:
        abort(404)
    else:
        # Usamos el metodo delete creado en cada storage
        storage.delete(review)
        # Guardamos los cambios
        storage.save()
        # Se devuelve un diccionario vacio y se retorna status 200
        return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
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

    # Traemos state por su "id"
    palce = storage.get(Place, place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place is None:
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
    if "text" not in body:
        return (jsonify({'error': 'Missing text'}), 400)

    # Si se paso "text" y "user_id" se crea el objeto y se guarda en la base de
    # datos Se crea el nuevo objeto pasandole como "kwargs" el diccionario que
    # traemos con la request en "body".
    # Se agrega las "id" al dic "body", ya que en el body de la request
    # solo se mandan los datos de json no esta la id de state_id en el body
    body['place_id'] = place_id
    body['user_id'] = user_id

    # Se crea una instancia de la clase Review
    obj = Review(**body)

    storage.new(obj)
    # Se guarda el nuevo objeto dentro del storage
    storage.save()

    # Se devuelve el objeto creado y un status code de 201
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review_id(review_id):
    """
    Make a POST request HTTP to update data.
    """
    # Hacemos la request de la data que se pase en formato json y la
    # pasamos a un dic de python para poder trabajar con ella
    body = request.get_json()

    # If the HTTP request body is not valid JSON, raise a 400 error
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # Se trae el objeto del review que se pase la "id"
    review = storage.get(Review, review_id)

    # If the review_id is not linked to any Review object, raise a 404 error
    if review is None:
        abort(404)
    else:
        # keys to ignore - not change
        keys_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]

        for key, value in body.items():
            if key not in keys_ignore:
                setattr(review, key, value)
            else:
                pass
        # Se guarda el nuevo objeto dentro del storage
        storage.save()
        # Se devuelve el objeto creado y un status code de 200
        return make_response(jsonify(review.to_dict()), 200)
