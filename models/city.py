#!/usr/bin/python3
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city.
        attributes:
            state_id (str): state id
            name (str): name of the city
    """
    state_id = ""
    name = ""
