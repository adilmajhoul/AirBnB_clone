#!/usr/bin/python3
"""defines the HBNBCommand class"""
import cmd
import re
from shlex import split
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models import storage

def parse_arg(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """represents the entry point of the command interpreter"""
    prompt = '(hbnb) '
    __models_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }
    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """empty line + ENTER shouldn’t execute anything"""
        pass
    
    def parse_arg(self, arg):
        """parse the arg"""
        args = arg.split()
        if len(args) == 0:
            return None
        if args[0] not in self.__models_classes:
            return None
        return args[0]

    def do_create(self, arg):
        """Create a new instance of BaseModel and print the id"""
        model = parse_arg(arg)
        if len(model) == 0:
            print("** class name missing **")
            return
        elif model[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
            return
        else:
            print(eval(model[0])().id)
            print(model[0])
            storage.save()

    def do_show(self, arg):
        """show the string representation of an instance"""
        arg = parse_arg(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        elif "{}.{}".format(arg[0], arg[1]) not in obj:
            print("** no instance found **")
            return
        else:
            print(obj["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, arg):
        """destroy an instance"""
        arg = parse_arg(arg)
        print(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif arg[0] not in self.__models_classes:
            print("** class doesn't exist **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        elif "{}.{}".format(arg[0], arg[1]) not in obj.keys():
            print("** no instance found **")
            return
        else:
            del obj["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, arg):
        """show all instances"""
        arg = parse_arg(arg)
        obj = storage.all()
        if len(arg) == 0:
            for key, value in obj.items():
                print(value)
        elif arg[0] not in self.__models_classes:
            print("** class doesn't exist **")
            return
        else:
            for key, value in obj.items():
                if arg[0] == value.__class__.__name__:
                    print(value)

    def do_update(self, arg):
        """update <class name> <id> <attribute name> "<attribute value>"""
        arg = parse_arg(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
            return False
        elif arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
            return False
        elif len(arg) == 1:
            print("** instance id missing **")
            return False
        elif "{}.{}".format(arg[0], arg[1]) not in obj.keys():
            print("** no instance found **")
            return False
        elif len(arg) == 2:
            print("** attribute name missing **")
            return False
        elif len(arg) == 3:
            try:
                type(eval(arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg) == 4:
            ob = obj["{}.{}".format(arg[0], arg[1])]
            if arg[2] in ob.__class__.keys():
                valtype = type(ob.__class__[arg[2]])
                ob.__dict__[arg[2]] = valtype(arg[3])
            else:
                ob.__dict__[arg[2]] = arg[3]
        elif type(eval(arg[2])) == dict:
            ob = obj["{}.{}".format(arg[0], arg[1])]
            for key, value in arg[2].items():
                if key in ob.__class__.keys():
                    valtype = type(ob.__class__[key])
                    ob.__dict__[key] = valtype(value)
                else:
                    ob.__dict__[key] = value
        storage.save()

    def do_clear(self, arg):
        """clear the console"""
        os.system("clear")


if __name__ == '__main__':
    HBNBCommand().cmdloop()