#!/usr/bin/python3

"""Display HTML page 6-index.html"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def filters():
    """Display,states, cities and amenities"""
    states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    return render_template("10-hbnb_filters.html", states=states,
                           amenities=amenities)


@app.teardown_appcontext
def tear_down(exception):
    """Ends Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
