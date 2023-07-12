#!/usr/bin/pyhton3
"""This module defines a class `user`"""

from models.base_model import BaseModel


class User(BaseModel):
    '''Defines a user'''
    email = ""
    password = ""
    first_name = ""
    last_name = ""
