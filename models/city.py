#!/usr/bin/pyhton3
"""This module defines a class `City`"""

from models.base_model import BaseModel


class City(BaseModel):
    '''Defines a City'''
    state_id = ""
    name = ""
