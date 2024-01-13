#!/usr/bin/python3
"""
base model of our airBnB
"""

from datetime import datetime
import models
from uuid import uuid4


class BaseModel:
    """
    Define BaseModel class
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the `BaseModel` object.

        Args:
            *args: Additional positional arguments (if any).
            **kwargs: Additional keyword arguments (if any).

        Attributes:
            id (str): The unique identifier of the object.
            created_at (datetime): time of creation
            updated_at (datetime): time of updates
        """
        if kwargs:
            for key in kwargs:
                if key == "__class__":
                    pass
                elif key == "id":
                    self.id = kwargs[key]
                elif key == "created_at":
                    self.created_at = datetime.strptime(kwargs[key], "\
%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(kwargs[key], "\
%Y-%m-%dT%H:%M:%S.%f")
                else:
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.the_storage.new(self)

    def __str__(self):
        """
        string method that return descriptor of the object
        Return:
            object descriptor
        """
        return ("[{}] ({}) {}\
".format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        """
        save is a method that save time of updates and update
        the updated_at instance attribute
        """
        self.updated_at = datetime.now()
        models.the_storage.save()

    def to_dict(self):
        """
        to_dict is a method that get an prepared dict
        Return:
             my_dic
        """
        my_dic = {}
        for key in self.__dict__:
            my_dic[key] = self.__dict__[key]
        my_dic["__class__"] = self.__class__.__name__
        my_dic["created_at"] = self.created_at.isoformat()
        my_dic["updated_at"] = self.updated_at.isoformat()
        return my_dic

