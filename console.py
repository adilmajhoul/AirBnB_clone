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
            lexer = split(arg[: brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[: curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """represents the entry point of the command interpreter"""

    prompt = "(hbnb) "
    __models_classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review",
    }

    def diff_syntax(self, arg):
            """Method to take care of following commands:
            <class name>.all()
            <class name>.count()
            ... (other commands)
            """
            new_syntax = {
                "all": self.do_all,
                "count": self.do_count,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update,
                "create": self.do_create,
            }
            match = re.search(r"\.", arg)
            if match is not None:
                argu = [arg[:match.span()[0]], arg[match.span()[1]:]]
                if argu[1] == "all()" or argu[1] == "all":
                    if argu[0] in HBNBCommand.__models_classes:
                        return self.do_all(argu[0])
                    else:
                        print("** Class doesn't exist **")
                match = re.search(r"\((.*?)\)", argu[1])
                if match is not None:
                    command = [argu[1][:match.span()[0]], match.group()[1:-1]]
                    if command[0] in new_syntax.keys():
                        call = "{} {}".format(argu[0], command[1])
                        if argu[0] in HBNBCommand.__models_classes:
                            return new_syntax[command[0]](call)
                        else:
                            print("** Class doesn't exist **")
            print("*** Unknown syntax: {}".format(arg))
            return False


    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the program"""
        print()  # ! new line could be error
        return True

    def emptyline(self):
        """empty line + ENTER shouldn’t execute anything"""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel and print the id"""
        model = parse_arg(arg)
        if len(model) == 0:
            print("** class name missing **")
        elif model[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
        else:
            print(eval(model[0])().id)
            storage.save()

    def do_show(self, arg):
        """show the string representation of an instance"""
        arg = parse_arg(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj:
            print("** no instance found **")
        else:
            print(obj["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, arg):
        """destroy an instance"""
        arg = parse_arg(arg)
        print(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in self.__models_classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj.keys():
            print("** no instance found **")
        else:
            del obj["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, arg):
        """show all instances"""
        argu = parse_arg(arg)
        if len(argu) > 0 and argu[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argu) > 0 and argu[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argu) == 0:
                    objl.append(obj.__str__())
            print(objl)

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
                valuetyp = type(ob.__class__.__dict__[arg[2]])
                ob.__dict__[arg[2]] = valuetyp(arg[3])
            else:
                ob.__dict__[arg[2]] = arg[3]
        elif type(eval(arg[2])) == dict:
            ob = obj["{}.{}".format(arg[0], arg[1])]
            for key, value in eval(arg[2]).items():
                if key in ob.__class__.__dict__.keys() and type(
                    ob.__class__.__dict__[key]
                ) in {str, int, float}:
                    valuetyp = type(ob.__class__.__dict__[key])
                    ob.__dict__[key] = valuetyp(value)
                else:
                    ob.__dict__[key] = value
        storage.save()

    def do_count(self, arg):
        """count the number of instances"""
        arg = parse_arg(arg)
        obj = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__models_classes:
            print("** class doesn't exist **")
        else:
            count = 0
            for key in obj.values():
                if arg[0] == key.__class__.__name__:
                    count += 1
            print(count)



    def do_clear(self, arg):
        """clear the console"""
        os.system("clear")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
