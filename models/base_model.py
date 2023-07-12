#!/usr/bin/python3
"""
This module defines the BaseModel class
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Base class for other models.

    Attributes:
        id (str): Unique identifier for the instance.
        created_at (datetime): Date & time when the instance was created.
        updated_at (datetime): Date & time when the instance was last updated.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.

        The id is set to a unique identifier generated using UUID.
        The created_at & updated_at attributes are set to current date & time.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    # skip this attribute
                    continue
                if key == "created_at" or key == "updated_at":
                    # convert value from string to datetime object
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

                # set attribute of object using key & value
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

            # save the new instance to storage
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: String representation of the instance in the format:
                "[ClassName] (id) dictionary_representation"
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the updated_at attribute with the current date and time
        & saves it to storage

        This method is called to mark when an instance is updated.
        """

        # save the time of update
        self.updated_at = datetime.now()

        # save the object to storage
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the BaseModel instance.

        The dictionary contains all the attributes of the instance,
        including the class name, id, created_at, and updated_at converted
        to ISO 8601 format.

        Returns:
            dict: Dictionary representation of the instance.
        """

        # create a shallow copy of __dict__ for modification
        new_dict = self.__dict__.copy()

        # add a __class__ field
        new_dict["__class__"] = self.__class__.__name__

        # modify the created_at & updated_fields from datetime
        # objects into strings in ISO format
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()

        return new_dict
