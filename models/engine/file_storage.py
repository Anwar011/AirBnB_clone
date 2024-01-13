#!/usr/bin/python3
"""
a file_storage that manages
our storage
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    define a class
    FileStorage that manage objects storage
    attributes:
        __file_path (str): file storage path
        __objects (dict): my_dic of object created
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ get objects of the class """
        return FileStorage.__objects

    def new(self, obj):
        """ Add new object to objects my_dic """
        FileStorage.__objects["{}.{}\
".format(obj.to_dict()['__class__'], obj.id)] = obj

    def save(self):
        """ Save objects to json file """
        my_dic = {}
        for key in FileStorage.__objects:
            my_dic[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, "w") as file:
            file.write(json.dumps(my_dic))

    def reload(self):
        """ load objects from json file """
        try:
            with open(FileStorage.__file_path, "r") as file:
                my_dic = json.loads(file.read())
            for key in my_dic:
                self.new(eval(my_dic[key]["__class__"])(**my_dic[key]))
        except IOError:
            pass

