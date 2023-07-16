#!/usr/bin/python3

"""HBNBCommand Class"""
import cmd
import shlex
import re
import json
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):

    """A HBNBCommand class"""
    prompt = '(hbnb) '

    def __class_validity(self, arguments):

        arguments = re.split(r" (?![^{}[\]()]*[}\]])", arguments)
        if len(arguments) == 0:
            print("** class name missing **")
            return None

        if arguments[0] not in globals().keys():
            print("** class doesn't exist **")
            return None

        return arguments

    def __func(self, cmd_text, arguments):

        arguments = self.__class_validity(arguments)
        if arguments is None:
            return

        if len(arguments) < 2:
            print("** instance id missing **")
            return

        storage.reload()
        objects = storage.all()
        key = arguments[0] + '.' + arguments[1]

        if key not in objects.keys():
            print("** no instance found **")
        elif cmd_text == "destroy":
            del objects[key]
            storage.save()
        else:
            print(objects[key])

    def __parse(self, arg_str):
        parsed_argument = re.split(r"\(|, (?![^{}[\]()]*[}\]])", arg_str[:-1])
        return parsed_argument

    def __get_instances(self, objects, classname):
        objects_array = []
        for key in objects.keys():
            class_type = key.split('.')[0]
            if class_type == classname:
                objects_array.append(str(objects[key]))
        return objects_array

    def do_quit(self, arg):
        'Quit command to exit the program'
        return True

    def do_EOF(self, arg):
        'EOF command to exit the program'
        return True

    def do_create(self, arguments):
        'Creates a new Instance of a class'
        arguments = self.__class_validity(arguments)
        if arguments is None:
            return
        obj = globals()[arguments[0]]()
        print(obj.id)

    def do_show(self, arguments):
        'Prints the string repr of an instance based on the class name and id'
        self.__func("show", arguments)

    def do_destroy(self, arguments):
        'Deletes an instance based on the class name and id'
        self.__func("destroy", arguments)

    def do_count(self, arguments):
        'Retrieves the number of instances of a class'
        arguments = self.__class_validity(arguments)
        if arguments is None:
            return
        storage.reload()
        objects = storage.all()
        print(len(self.__get_instances(objects, arguments[0])))

    def do_all(self, arguments):
        """
        Prints all string repr of all instances based on the class name
        """
        arguments_count = len(shlex.split(arguments))

        storage.reload()
        objects = storage.all()
        objects_arr = []

        if arguments_count < 1:
            for value in objects.values():
                objects_arr.append(str(value))
        else:
            arguments = self.__class_validity(arguments)
            if arguments is None:
                return
            else:
                objects_arr = self.__get_instances(objects, arguments[0])

        print(objects_arr)

    def do_update(self, arguments):
        """Updates an instance based on the class name and id"""
        arguments = self.__class_validity(arguments)
        if arguments is None:
            return
        elif len(arguments) < 2:
            print("** instance id missing **")
            return

        storage.reload()
        objects = storage.all()
        key = arguments[0] + '.' + arguments[1]

        if key not in objects.keys():
            print("** no instance found **")
            return
        elif len(arguments) < 3:
            print("** attribute name missing **")
            return
        elif '}' in arguments[2]:
            for key, value in eval(arguments[2]).items():
                argument = f"{arguments[0]} {arguments[1]} {key} {value}"
                self.do_update(argument)
            return
        elif len(arguments) < 4:
            print("** value missing **")
            return
        else:
            obj = vars(objects[key])
            attr = arguments[2]
            value = arguments[3]
            if attr in obj.keys():
                attr_type = type(obj[attr])
                value = attr_type(arguments[3])
            obj[attr] = value
            objects[key].save()

    def precmd(self, arguments):
        if "." in arguments:
            arguments = arguments.split('.', 1)
            classname = arguments[0]
            arguments = self.__parse(arguments[1])
            function = arguments[0]
            line = f"{function} {classname} {(' ').join(arguments[1:])}"
            return cmd.Cmd.precmd(self, line)
        else:
            return cmd.Cmd.precmd(self, arguments)
        return

    def emptyline(self):
        'Does nothing'
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
