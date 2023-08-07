#!/usr/bin/python3
"""defines the HBNBCommand class"""
import cmd
from models.base_model import BaseModel
from models import storage


def prase_arg(self, arg):
    """parse the arg"""
    args = arg.split()
    if len(args) == 0:
        return None
    if args[0] not in self.__models_classes:
        return None
    return args[0]
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
    
    def do_create(self, arg):
        """create a new instance of BaseModel and prints the id"""
        model = prase_arg(arg)
        if model is None:
            print("** class name missing **")
            return
        obj = eval(model)()
        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """show the BaseModel instance with the id"""
        model = prase_arg(arg)
        if len(model) == 0:
            print("** class name missing **")
            return
        elif model[0] not in HBNBCommand.__models_classes:
            print("** class name missing **")
            return
        elif len(model) == 1:
            print("** instance id missing **")
            return
        elif "{}.{}".format(model[0], model[1]) not in storage.all():
            print("** no instance found **")
            return
        else:
            print(storage.all()["{}.{}".format(model[0], model[1])])


if __name__ == '__main__':
    HBNBCommand().cmdloop()