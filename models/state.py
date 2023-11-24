#!/usr/bin/python3
""" Holds class State """
import models
from models.base_model import BaseModel, Base
from models.city import City
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ Representation of a state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City",
            backref="state",
            cascade=["all", "delete-orphan"])
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """ Initializes state """
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """ Getter for a list of city
            instances related to the state """
            return [
                city for city in models.storage.all(City).values()
                if city.state_id == self.id
                ]
