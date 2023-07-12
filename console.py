#!/usr/bin/python3
"""
This module defines HBNBCommand, the entry
point of the command interpreter
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = ["BaseModel", "User", "State", "City", "Place", "Amenity", "Review"]


class HBNBCommand(cmd.Cmd):
    """ The HBNBCommand class """
    prompt = "(hbnb) "

    def do_quit(self, line):
        """quit command exits the program
        """
        return True

    def do_EOF(self, line):
        """EOF signal exits the program
        """
        print()  # adds a newline after EOF
        return True

    def emptyline(self):
        """ When empty line is encountered, do nothing """
        pass

    def do_create(self, line):
        """Creates a new instance of a class, saves it to storage
        and prints the id
        """
        line = line.split()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in classes:
            print("** class doesn't exist **")
        else:
            instance = eval(line[0])()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on the
        class name and id
        """
        line = line.split()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in classes:
            print("** class doesn't exist **")
        elif len(line) == 1:
            print("** instance id missing **")
        else:
            instance_key = f'{line[0]}.{line[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[instance_key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name id
        """
        line = line.split()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in classes:
            print("** class doesn't exist **")
        elif len(line) == 1:
            print("** instance id missing **")
        else:
            instance_key = f'{line[0]}.{line[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[instance_key]
                storage.save()

    def do_all(self, line):
        """Print all string representation of all instance based or
        not on the class name
        """
        line = line.split()
        if len(line) == 0:
            # print all objects in storage
            if len(storage.all()) > 0:
                print("[", end="")
                for index, obj in enumerate(storage.all().values()):
                    print('"', end="")
                    print(obj, end="")
                    print('"', end="")
                    if index != len(storage.all()) - 1:
                        print(", ", end="")
                print("]")
        elif line[0] not in classes:
            print("** class doesn't exist **")
        else:
            # print objects of a particular class in storage
            objects = []
            for key in storage.all():
                if key.startswith(line[0]):
                    objects.append(storage.all()[key])
            if len(objects) > 0:
                print("[", end="")
                for index, obj in enumerate(objects):
                    print('"', end="")
                    print(obj, end="")
                    print('"', end="")
                    if index != len(objects) - 1:
                        print(", ", end="")
                print("]")

    def do_update(self, line):
        """Updates an instance based on the class name and id
        by adding or updating attribute
        """
        line = line.split()
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in classes:
            print("** class doesn't exist **")
        elif len(line) == 1:
            print("** instance id missing **")
        elif len(line) == 2:
            instance_key = f'{line[0]}.{line[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                print("** attribute name missing **")
        elif len(line) == 3:
            print("** value missing **")
        else:
            instance_key = f'{line[0]}.{line[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                obj = storage.all()[instance_key]
                try:
                    setattr(obj, line[2], eval(line[3]))
                except NameError:
                    setattr(obj, line[2], line[3])
                obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
