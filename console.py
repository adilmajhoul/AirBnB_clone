#!/usr/bin/python3
"""defines the HBNBCommand class"""
import cmd
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage



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
        model = self.parse_arg(arg)
        if model is None:
            print("** class name missing **")
            return
        else:
            obj = eval(model)()
            obj.save()
            print(obj.id)
            storage.save()
            print(model)

    def do_show(self, arg):
        """show the string representation of an instance"""
        arg = self.parse_arg(arg)
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
            print("{} {}".format(arg[0], arg[1]))

    def do_destroy(self, arg):
        """destroy an instance"""
        arg = self.parse_arg(arg)
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
        arg = self.parse_arg(arg)
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
        arg = self.parse_arg(arg)
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