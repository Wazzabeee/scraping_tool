#!/usr/bin/env python
""" This module launches the GUI of this program

This modules creates the tkinter object and defines the window theme.
See more about window definition in menu.py

"""

from tkinter import Tk

from menu import Menu


def main():
    """ Runs the window mainloop and sets theme """
    print("[Main]")
    root = Tk()
    root.call("source", "../theme/sun-valley.tcl")
    root.call("set_theme", "dark")
    Menu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
