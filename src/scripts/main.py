from tkinter import Tk

from menu import Menu


def main():
    print("[Main]")
    root = Tk()
    root.call("source", "../theme/sun-valley.tcl")
    root.call("set_theme", "dark")
    app = Menu(root)
    root.mainloop()


if __name__ == '__main__':
    main()
