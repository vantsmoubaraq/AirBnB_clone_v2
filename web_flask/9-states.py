#!/usr/bin/python3
""" Script starts a Flask Web Application
listening on 0.0.0.0, port 5000
"""

from flask import Flask, render_template
import models
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """Displays HTML of all States in Stored Chronologically"""
    states = models.storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def list_state_cities():
    """Displays HTML of states and its cities"""
    states = models.storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
def list_states():
    """Displays HTML of states Chronologically"""
    states = models.storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_id(id):
    """Displays HTML of States based on id"""
    flag = 0
    states = None
    all_states = models.storage.all(State).values()
    for state in all_states:
        if id in state.id:
            flag = 1
            states = state
            break
    return render_template('9-states.html', states=states, flag=flag)


@app.teardown_appcontext
def teardown(db):
    """Closes or otherwise deallocates resource if it exists"""
    models.storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
