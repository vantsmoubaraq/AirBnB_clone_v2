#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    if models.storage_type == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer(), nullable=False, default=0)
        number_bathrooms = Column(Integer(), nullable=False, default=0)
        max_guest = Column(Integer(), nullable=False, default=0)
        price_by_night = Column(Integer(), nullable=False, default=0)
        latitude = Column(Float(), nullable=True)
        longitude = Column(Float(), nullable=True)
        reviews = relationship("Review", backref="place", cascade="all, delete")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __int__(self, *args, **kwargs):
        """initialises Place"""
        super().__int__(*args, **kwargs)

    if models.storage_type != 'db':
        @property
        def reviews(self):
            from models.review import Review
            """File Storage relationship between Reviews & Place"""
            review_list = []
            all_reviews = models.storage.all(Review)
            for city in all_reviews.values():
                if Review.place_id == self.id:
                    review_list.append(city)
            return review_list
