#!/usr/bin/python3
""" basemodel the mother of all models """

import models
from uuid import uuid4
from datetime import datetime
import json


class BaseModel:
    """ the base model which all other models inherit from """

    def __init__(self, *args, **kwargs):
        """ base model constructor """

        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        time_format = "%Y-%m-%dT%H:%M:%S.%f"

        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value

    def __str__(self):
        """ class string representation """
        class_name = self.__class__.__name__
        string = f"[{class_name}] ({self.id}) {self.__dict__}"
        return string

    def save(self):
        """ update the last updated time to now """
        self.updated_at = datetime.today()

    def to_dict(self):
        """ create new dict for its current class """
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        new_dict["__class__"] = self.__class__.__name__
        return new_dict