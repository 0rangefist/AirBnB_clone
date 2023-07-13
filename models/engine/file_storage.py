#!/usr/bin/python3
"""
This module defines the FileStorage class
"""
import json
import os
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    The FileStorage class serializes instances to a JSON file
    and deserializes JSON file to instances:
    """

    # path to the JSON file
    __file_path = "file.json"

    #  store all objects by <class name>.id
    __objects = {}

    def all(self):
        """ Returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """

        object_dictionaries = {}
        # convert objects in __objects into their dictionary representations
        for key, value in self.__objects.items():
            object_dictionaries[key] = value.to_dict()

        # write the object_dictionaries into a serializable json file
        with open(self.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(object_dictionaries, json_file)

    def reload(self):
        """  deserializes the JSON file to __objects if file exists """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                # load the dict rep of objects back from json file
                object_dictionaries = json.load(json_file)
                # convert each dict rep back into an object
                # and save it in __objects
                for dict_ in object_dictionaries.values():
                    class_name = dict_["__class__"]
                    # eval is used to create a new object from class_name
                    # the object is initialised using the dict as kwargs
                    obj = eval(class_name)(**dict_)
                    # the object is saved in __objects using new()
                    self.new(obj)
        except FileNotFoundError:
            pass
