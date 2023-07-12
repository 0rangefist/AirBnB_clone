#!/usr/bin/pyhton3
"""This module defines a class `Review`"""

from models.base_model import BaseModel


class Review(BaseModel):
    '''Defines a Review'''
    place_id = ""
    user_id = ""
    text = ""
