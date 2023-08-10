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

    def diff_syntax(self, arg):
        """Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)

        Description:
            Creates a list representations of functional models
            Then use the functional methods to implement user
            commands, by validating all the input commands
        """
        new_syntax = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        match = re.search(r"\.(.*?)\(", arg)
        if match is not None:
            arg = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg[1])
            if match is not None:
                cmd = [arg[1][:match.span()[0]], match.group()[1:-1]]
                if cmd[0] in new_syntax.keys():
                    cl = "{} {}".format(arg[0], cmd[1])
                    return new_syntax[cmd[0]](cl)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """empty line + ENTER shouldn’t execute anything"""
        pass

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
        if arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
            return
        if len(arg) == 1:
            print("** instance id missing **")
            return
        if "{}.{}".format(arg[0], arg[1]) not in obj:
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
        if arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
            return False
        if len(arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg[0], arg[1]) not in obj.keys():
            print("** no instance found **")
            return False
        if len(arg) == 2:
            print("** attribute name missing **")
            return False
        if len(arg) == 3:
            try:
                type(eval(arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg) == 4:
            ob = obj["{}.{}".format(arg[0], arg[1])]
            if arg[2] in ob.__class__.__dict__.keys():
                valtype = type(ob.__class__.__dict__[arg[2]])
                ob.__dict__[arg[2]] = valtype(arg[3])
            else:
                ob.__dict__[arg[2]] = arg[3]
        elif type(eval(arg[2])) == dict:
            ob = obj["{}.{}".format(arg[0], arg[1])]
            for key, value in eval(arg[2]).items():
                if (key in ob.__class__.__dict__.keys() and
                        type(ob.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(ob.__class__.__dict__[key])
                    ob.__dict__[key] = valtype(value)
                else:
                    ob.__dict__[key] = value
        storage.save()

    def do_count(self, arg):
        """count the number of instances"""
        arg = parse_arg(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
            return
        else:
            count = 0
            for key, value in obj.items():
                if arg[0] == value.__class__.__name__:
                    count += 1
            print(count)

    def do_clear(self, arg):
        """clear the console"""
        os.system("clear")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
