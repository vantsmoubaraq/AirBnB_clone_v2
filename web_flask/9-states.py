#!/usr/bin/python3

"""Display all states or one state if it has id"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def all_states():
    """Display all states"""
    states = list(storage.all(State).values())
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def one_state(id):
    """Display one state"""
    states = list(storage.all(State).values())
    return render_template("9-states.html", states=states, id=id)


@app.teardown_appcontext
def tear_down(exception):
    """Ends Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
