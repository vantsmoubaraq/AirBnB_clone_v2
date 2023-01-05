#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage
from models.city import City
from models import HBNB_TYPE_STORAGE


class State(BaseModel):
    """ State class """
    if HBNB_TYPE_STORAGE == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""


@property
def cities(self):
    """File Storage relationship between Cities & State"""
    city_list = []
    all_cities = storage.all(City)
    for city in all_cities.values():
        if city.state_id == self.id:
            city_list.append(city)
    return city_list
