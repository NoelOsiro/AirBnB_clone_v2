#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine, session, and links to MySQL database"""
        # Retrieve MySQL environment variables
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", default="localhost")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        # Set up the connection string
        connection_str = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            user, pwd, host, db)

        # Create the engine
        self.__engine = create_engine(connection_str, pool_pre_ping=True)

        # Drop all tables if environment is 'test'
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        # Create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create a scoped session with the engine
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def all(self, cls=None):
        """Query on the current database
        session all objects depending on class name"""
        objects_dict = {}
        classes = [User, State, City, Amenity, Place, Review]

        if cls:
            classes = [cls]

        for c in classes:
            objects = self.__session.query(c).all()
            for obj in objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects_dict[key] = obj

        return objects_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))
