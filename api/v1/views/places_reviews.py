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
    Return state objects by id or 404 if the id does not exists
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
