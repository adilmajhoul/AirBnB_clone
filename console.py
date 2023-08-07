#!/usr/bin/python3
"""defines the HBNBCommand class"""
import cmd
from models.base_model import BaseModel
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

    def prase_arg(self, arg):
        """parse the arg"""
        args = arg.split()
        if len(args) == 0:
            return None
        if args[0] not in self.__models_classes:
            return None
        return args[0]
    
    def do_create(self, arg):
        """create a new instance of BaseModel and prints the id"""
        model = self.prase_arg(arg)
        if model is None:
            print("** class name missing **")
            return
        obj = eval(model)()
        obj.save()
        print(obj.id)

    


if __name__ == '__main__':
    HBNBCommand().cmdloop()