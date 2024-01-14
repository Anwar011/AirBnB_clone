#!/usr/bin/python3
"""
Module of AIRBNB console
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
from models import the_storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import shlex
import sys
import json


class HBNBCommand(cmd.Cmd):
    """
    define HBNBCommand class

    Classe Attributes:
        prompt (str): The prompt.
        classes_list (list): A list of all used class names.
    """

    prompt = "(hbnb) "
    classes_list = ["BaseModel", "User", "State", "City\
", "Amenity", "Place", "Review"]

    def do_create(self, line):
        """create is a command to creates a new instance\n"""
        className = line.split()
        if len(className) == 0:
            print("** class name missing **")
        elif className[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
        else:
            new_object = eval(className[0])()
            the_storage.save()
            print(new_object.id)

    def check_id(self, line):
        """
        check if class name and id exist or not
        """
        lines_list = shlex.split(line)
        if len(lines_list) == 0:
            print("** class name missing **")
            return False
        if lines_list[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return False
        if len(lines_list) < 2:
            print("** instance id missing **")
            return False
        if lines_list[0]+"."+lines_list[1] in the_storage.all():
            return True
        print("** no instance found **")

    def check_attr(self, line):
        """
        check if attribute name exist or not
        """
        lines_list = shlex.split(line)
        if len(lines_list) < 3:
            print("** attribute name missing **")
            return False
        if len(lines_list) < 4:
            print("** value missing **")
            return False
        return True

    def do_show(self, line):
        """show is a command to print object representation"""
        lines_list = shlex.split(line)
        if self.check_id(line):
            print(the_storage.all()["{}.{}\
".format(lines_list[0], lines_list[1])])

    def do_destroy(self, line):
        """destroy is a command that destroy object"""
        lines_list = shlex.split(line)
        if self.check_id(line):
            del the_storage.all()["{}.{}\
".format(lines_list[0], lines_list[1])]
            the_storage.save()

    def do_all(self, line):
        """all is a command that prints all objects representation """
        # TODO: all BaseModel dgf
        if line == "":
            list_str = []
            for key in the_storage.all():
                list_str.append(str(the_storage.all()[key]))
            print(list_str)
        else:
            if line.split()[0] in HBNBCommand.classes_list:
                list_str = []
                for key in the_storage.all():
                    if line.split()[0] in key:
                        list_str.append(str(the_storage.all()[key]))
                print(list_str)
            else:
                print("** class doesn't exist **")

    def do_update(self, line):
        """update command that update an object"""
        if self.check_id(line):
            if self.check_attr(line):
                lines_list = shlex.split(line)
                obj = the_storage.all()[f"{lines_list[0]}.{lines_list[1]}"]
                if hasattr(obj, lines_list[2]):
                    # TODO: handle casting error by using try except
                    try:
                        value = type(getattr(obj, lines_list[2]))
                        (lines_list[3])
                        setattr(obj, lines_list[2], value)
                    except ValueError:
                        pass
                else:
                    value = lines_list[3]
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        value = lines_list[3]
                    setattr(obj, lines_list[2], value)
                obj.save()

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, line):
        """C-d command to exit the program\n"""
        return True

    def emptyline(self):
        """an empty line handling"""
        pass

    def default(self, line):
        """
        default commands
        """
        if line.endswith(".all()"):
            """
            Check if the command matches
            <class_name>.all()
            """
            if line[:-6] != "":
                self.do_all(line[:-6])
        elif line.endswith(".count()"):
            """
            Check if the command matches
            <class_name>.count()
            """
            if line[:-8] != "":
                if line[:-8] in HBNBCommand.classes_list:
                    num_obj = 0
                    for key in the_storage.all():
                        if line[:-8] in key:
                            num_obj += 1
                    print(num_obj)
                else:
                    print("** class doesn't exist **")

        elif ".show(" in line and line.endswith(")"):
            """
            Check if the command matches
            <class_name>.show(<id>)
            """
            className = line.split(".")[0]
            id = line.split("(")[1][:-1]
            self.do_show(className+" "+id)

        elif ".destroy(" in line and line.endswith(")"):
            """
            Check if the command matches
            <class_name>.destroy(<id>)
            """
            className = line.split(".")[0]
            id = line.split("(")[1][:-1]
            self.do_destroy(className+" "+id)

        elif ".update(" in line and line.endswith(")"):
            className = line.split(".")[0]
            lines = line.split("(")[1][:-1]
            if "{" in lines and lines.endswith("}"):
                id = lines.split(", ")[0]
                str_dict = "{"+lines.split("{")[1]
                dictionary = dict(eval(str_dict))
                string = className+" "+id
                for attr in dictionary:
                    self.do_update(string+" \
"+attr+" "+"\""+str(dictionary[attr])+"\"")
            else:
                string = className
                for elm in lines.split(", "):
                    string += " "+elm
                self.do_update(string)
        else:
            print("*** Unknown syntax: "+line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
