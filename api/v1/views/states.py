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


@app_views.route("/states", methods=['GET'])
def return_states():
    """
    Return states - use GET request
    No es necesario poner la opcion methods aca ya que GET se hace por default,
    lo ponemos por mayor claridad nomas.
    """
    states = storage.all(State)

    for key, value in states.items():
    # Si las ID coinciden se retorna el value que es la
    # representacion del string del objeto
            return value.to_dict()
