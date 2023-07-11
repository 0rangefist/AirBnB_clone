#!/usr/bin/python3
"""
This module defines HBNBCommand, the entry
point of the command interpreter
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """ The HBNBCommand class """
    prompt = "(hbnb) "

    def do_quit(self, line):
        """quit exits the program"""
        return True

    def do_EOF(self, line):
        """EOF exits the program"""
        print()  # adds a newline after EOF
        return True

    def emptyline(self):
        """ When empty line is encountered, do nothing """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
