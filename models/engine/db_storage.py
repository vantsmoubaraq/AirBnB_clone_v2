#!/usr/bin/python3

"""
Module implements New engine DBStorage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import inspect
from os import getenv


class DBStorage:
    """
    class implements New engine DBStorage
    """
    __engine = None
    __session = None

    classes = {"Amenity": Amenity, "City": City, "Place": Place, "Review": Review, "State": State, "User": User}

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(getenv("HBNB_MYSQL_USER"), getenv("HBNB_MYSQL_PWD")                                      , getenv("HBNB_MYSQL_HOST"), getenv("HBNB_MYSQL_DB"), pool_pre_ping=True))
        
        if getenv("HBNB_ENV") == "test":
            meta = Metadata(self.__engine)
            meta.reflect()
            meta.drop_all()

    def all(self, cls=None):
        """
        return objects depending of the class name
        """
        objects = {}

        if cls in DBStorage.classes:
            results = self.__session.query(DBStorage.classes[cls]).all()

            for result in results:
                objects["{}.{}".format(result.__class__.__name__, result.id)] = result

            return objects

        for each in DBStorage.classes:
            results = self.__session.query(DBStorage.classes[each]).all()

            for result in results:
                objects["{}.{}".format(result.__class__.__name__, result.id)] = result
        return objects
    
    def new(self, obj):
        """
         add the object to the current database session
        """
        try:
            self.__session.add(obj)
        except Exception as e:
            self.__session.rollback()
            print(e)

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session 
        """
        if obj is not None:
            #result = session.query(obj.__class__.__name__).filter(obj.__class__.__name__ == obj.id).first()
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database 
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
