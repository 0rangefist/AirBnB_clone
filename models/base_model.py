#!/usr/bin/python3

import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for other models.

    Attributes:
        id (str): Unique identifier for the instance.
        created_at (datetime): Date and time when the instance was created.
        updated_at (datetime): Date and time when the instance was last updated.
    """

    def __init__(self):
        """
        Initializes a new instance of BaseModel.

        The id is set to a unique identifier generated using UUID.
        The created_at and updated_at attributes are set to the current date and time.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: String representation of the instance in the format:
                "[ClassName] (id) additional_info"
        """
        return "[{}] ({})".format(self.__class__.__name__, self.id)

    def save(self):
        """
        Updates the updated_at attribute with the current date and time.

        This method is called to mark the instance as updated.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary representation of the BaseModel instance.

        The dictionary contains all the attributes of the instance, including the class name,
        id, created_at, and updated_at converted to ISO 8601 format.

        Returns:
            dict: Dictionary representation of the instance.
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict
