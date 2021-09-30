import tkinter as tk
from tkinter import ttk
from window import ScraperWindow
from PIL import Image, ImageTk


class Menu:
    def __init__(self, master):
        self.master = master
        self.master.iconbitmap("../images/cobweb.ico")
        self.master.title("Scraping tool")
        self.frame = tk.Frame(self.master)

        self.buttons_frame = ttk.Frame(self.frame, borderwidth=1)

        inst = (Image.open('../images/instagram_logo.png'))
        inst_resized = inst.resize((60, 60), Image.ANTIALIAS)
        self.real_insta = ImageTk.PhotoImage(inst_resized)
        self.instagram_button = tk.Button(self.frame, text="Click me", width=60, height=60,
                                          image=self.real_insta)
        self.instagram_button["bg"] = "black"
        self.instagram_button["border"] = "0"
        self.instagram_button.grid(row=0, column=0)

        img = (Image.open('../images/twitter_logo.png'))
        resized = img.resize((60, 60), Image.ANTIALIAS)
        self.real_twitter = ImageTk.PhotoImage(resized)
        self.twitter_button = tk.Button(self.frame, text="Click me", width=60, height=60,
                                        image=self.real_twitter,
                                        command=self.twitter_window)
        self.twitter_button["bg"] = "black"
        self.twitter_button["border"] = "0"
        self.twitter_button.grid(row=0, column=1)

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
