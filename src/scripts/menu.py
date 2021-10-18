import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from window import ScraperWindow


class Menu:
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap("../images/cobweb.ico")
        self.master.title("Scraping tool")
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.master.update()
        self.center_window()

    def twitter_window(self):
        self.twitterWindow = tk.Toplevel(self.master)
        self.app = ScraperWindow(self.twitterWindow)

    def center_window(self):
        """ Centers the window on the screen based on screen size """

        win_width, win_height = self.master.winfo_width(), self.master.winfo_height()
        screen_width = int((self.master.winfo_screenwidth() - win_width) / 2)
        screen_height = int((self.master.winfo_screenheight() - win_height) / 2)
        self.master.geometry(f"{win_width}x{win_height}+{screen_width}+{screen_height}")
