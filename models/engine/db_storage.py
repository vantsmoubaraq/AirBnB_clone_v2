#!/usr/bin/python3
"""
Contains the Class DBStorage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity
from os import getenv


classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }


class DBStorage:
    """This is the Database Storage Engine class"""
    __engine = None
    __session = None

    def __int__(self):
        """Attribute Instantiation for DBStorage Object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieves all objects in Database queried based on class"""
        new_dict = {}
        if cls is None:
            for clus in classes.values():
                objs = self.__session.query(clus).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict.update({key: obj})
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict.update({key: obj})

        return new_dict

    def new(self, obj):
        """Adds object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of current database session"""
        self.__session.commit()

    def delete(self, obj):
        """Delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all objects"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

