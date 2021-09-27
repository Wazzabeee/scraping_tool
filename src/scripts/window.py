"""
This module is the GUI for Twitter API
@author : Clément Delteil
"""
from datetime import date, datetime, timedelta
from os import path
from tkinter import Tk, ttk, filedialog, messagebox, IntVar, StringVar, N, S, E, W, LEFT, Text, \
    END
from traceback import format_exc
from twitter import test_api
from utils import get_dict_key, separate_int_string


class ScraperWindow:
    """ This class represents the twitter api window """

    def __init__(self):
        """ Tkinter UI objects definitions """

        self.window = Tk()

        # Set window theme
        self.window.tk.call("source", "../theme/sun-valley.tcl")
        self.window.tk.call("set_theme", "dark")

        self.window.withdraw()
        self.window.title("Scraping tool")

        # Overwrite Tk callback exception to get message on the screen when error occures
        Tk.report_callback_exception = self.callback_error

        # All variables linked to user choices
        self.search_type_var = IntVar(None, 1)
        self.language = StringVar()
        self.geocode = StringVar()
        self.date = StringVar()
        self.save_type_var = IntVar(None, 1)
        self.size = IntVar()
        self.result_type_var = StringVar(None, "mixed")

        # All languages options available
        self.options = {
            "fr": "French",
            "en": "English",
            "es": "Spanish",
            "de": "German",
        }

        # Search type frame
        self.search_type_frame = ttk.Labelframe(
            self.window,
            text="Search type",
            borderwidth=1,
            padding="80 3 12 12"
        )
        self.form_frame = ttk.Labelframe(
            self.window, text="Search form", borderwidth=1, padding="3 3 12 12"
        )
        self.save_frame = ttk.Labelframe(
            self.window, text="Save", borderwidth=1, padding="3 3 12 12"
        )
        self.result_type_frame = ttk.LabelFrame(self.form_frame, padding="5 0 3 8")
        self.save_type_frame = ttk.Labelframe(self.save_frame, padding="5 0 3 8")

        self.language_drop = ttk.OptionMenu(
            self.form_frame, self.language, self.options['en'], *self.options.values()
        )

        self.language_label = ttk.Label(self.form_frame, text="Search language")
        self.date_label = ttk.Label(self.form_frame, text="Search until")
        self.geocode_label = ttk.Label(self.form_frame, text="Results near")
        self.size_label = ttk.Label(self.form_frame, text="Number of results")
        self.result_type_label = ttk.Label(self.form_frame, text="Result type")
        self.save_path_label = ttk.Label(self.save_frame, text="Save directory")
        self.save_type_label = ttk.Label(self.save_frame, text="Save format")
        self.query_label = ttk.Label(self.form_frame, text="Query")

        self.query_entry = Text(self.form_frame, width="50", height="5")
        self.until_entry = ttk.Entry(self.form_frame, textvariable=self.date)
        self.geocode_entry = ttk.Entry(self.form_frame, textvariable=self.geocode)
        self.size_entry = ttk.Entry(self.form_frame, textvariable=self.size)
        self.save_path_entry = ttk.Entry(self.save_frame, text="", width=55)

        self.mixed_check = ttk.Radiobutton(
            self.result_type_frame,
            text="Mixed",
            variable=self.result_type_var,
            value="mixed"
        )
        self.recent_check = ttk.Radiobutton(
            self.result_type_frame,
            text="Recent",
            variable=self.result_type_var,
            value="recent",
        )
        self.popular_check = ttk.Radiobutton(
            self.result_type_frame,
            text="Popular",
            variable=self.result_type_var,
            value="popular",
        )
        self.json_check = ttk.Radiobutton(
            self.save_type_frame,
            text="JSON",
            variable=self.save_type_var,
            value=1
        )
        self.csv_check = ttk.Radiobutton(
            self.save_type_frame,
            text="CSV",
            variable=self.save_type_var,
            value=2,
            state='disable'
        )
        self.seven_day_check = ttk.Radiobutton(
            self.search_type_frame,
            text="7 Days search",
            variable=self.search_type_var,
            value=1,
        )
        self.thirty_day_check = ttk.Radiobutton(
            self.search_type_frame,
            text="30 Days search",
            variable=self.search_type_var,
            value=2,
            state='disable'
        )
        self.full_archive_check = ttk.Radiobutton(
            self.search_type_frame,
            text="Full archive search",
            variable=self.search_type_var,
            value=3,
            state='disable'
        )

        self.browse_button = ttk.Button(
            self.save_frame,
            text="Browse",
            style="Accent.TButton",
            command=self.update_path,
        )
        self.search_button = ttk.Button(
            self.window,
            text="Search",
            style="Accent.TButton",
            command=self.search
        )

        self.search_type_frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10)
        self.seven_day_check.grid(row=1, column=1, sticky=S, padx=10, pady=10)
        self.thirty_day_check.grid(row=1, column=2, sticky=S, padx=10, pady=10)
        self.full_archive_check.grid(row=1, column=3, sticky=S, padx=10, pady=10)
        self.form_frame.grid(column=0, row=1, sticky=(N, W, E, S), padx=10, pady=10)
        self.language_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.language_drop.grid(column=1, row=0, pady=20, padx=10, sticky=W)
        self.date_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.until_entry.grid(row=1, column=1, sticky=W, padx=10, pady=10)
        self.geocode_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.geocode_entry.grid(row=2, column=1, sticky=W, padx=10, pady=10)
        self.size_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.size_entry.grid(row=3, column=1, sticky=W, padx=10, pady=10)
        self.result_type_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.result_type_frame.grid(row=4, column=1, pady=10, padx=10)
        self.mixed_check.pack(expand=True, side=LEFT)
        self.recent_check.pack(expand=True, side=LEFT)
        self.popular_check.pack(expand=True, side=LEFT)
        self.query_label.grid(row=5, column=0, sticky=W, padx=5, pady=5)
        self.query_entry.grid(row=5, column=1, sticky=W, padx=10, pady=10)
        self.save_frame.grid(column=0, row=2, sticky=(N, W, E, S), padx=10, pady=10)
        self.save_path_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.save_path_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.browse_button.grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.save_type_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.search_button.grid(row=3, column=0, sticky=N, padx=5, pady=5)
        self.save_type_frame.grid(row=1, column=1, pady=10, padx=10)
        self.json_check.pack(expand=True, side=LEFT)
        self.csv_check.pack(expand=True, side=LEFT)

        # Insert format values
        self.until_entry.insert(-1, "YYYY-MM-DD")
        self.geocode_entry.insert(-1, "XXX,YYY,ZZ")

        # Make window appear again
        self.window.update()  # Update default or saved values
        self.center_window()  # Center the window on the screen
        self.window.deiconify()
        self.window.iconbitmap("../images/cobweb.ico")  # Add icon to window
        self.bind_them()  # Bind events to objects

    def bind_them(self):
        """ This method binds events to Tkinter objects """

        self.size_entry.bind("<FocusOut>", self.validate_int)
        self.size_entry.bind("<FocusIn>", self.validate_int)
        self.size_entry.bind("<KeyRelease>", self.validate_int)

        self.save_path_entry.bind("<FocusOut>", self.validate_path)
        self.save_path_entry.bind("<FocusIn>", self.validate_path)
        self.save_path_entry.bind("<KeyRelease>", self.validate_path)

        self.until_entry.bind("<FocusIn>", self.validate_date)
        self.until_entry.bind("<FocusOut>", self.validate_date)
        self.until_entry.bind("<KeyRelease>", self.validate_date)

        self.geocode_entry.bind("<FocusIn>", self.validate_geocode)
        self.geocode_entry.bind("<FocusOut>", self.validate_geocode)
        self.geocode_entry.bind("<KeyRelease>", self.validate_geocode)

    def validate_geocode(self, *_):
        """ This method invalidates the entry if its content is not a valid geolocalization """

        if self.geocode_entry.get() == "":
            self.geocode_entry.state(["invalid"])
        else:
            try:
                geocode = self.geocode_entry.get()
                lat, long, rad = geocode.split(",")
                if not (lat == "" or long == "" or rad == ""):
                    if -90 <= int(lat) <= 90 and -180 <= int(long) <= 180:
                        radius, unit = separate_int_string(rad)
                        if radius.isnumeric() and (str(unit) == "km" or str(unit) == "mi"):
                            self.geocode_entry.state(["!invalid"])
                        else:
                            self.geocode_entry.state(["invalid"])
                    else:
                        self.geocode_entry.state(["invalid"])
                else:
                    self.geocode_entry.state(["invalid"])

            except ValueError:
                self.geocode_entry.state(["invalid"])

    def validate_date(self, *_):
        """ This method invalidates the entry if its content is not an valid date """

        if self.until_entry.get() == "":
            self.until_entry.state(["invalid"])
        else:
            try:
                datetime.strptime(self.until_entry.get(), '%Y-%m-%d')

                # checks if date is sooner than 7 days from today
                if datetime.strptime(self.until_entry.get(), '%Y-%m-%d') <= (datetime.today() -
                                                                             timedelta(days=8)):
                    self.until_entry.state(["invalid"])
                else:
                    self.until_entry.state(["!invalid"])
            except ValueError:
                self.until_entry.state(["invalid"])

    def validate_int(self, *_):
        """ This method invalidates the entry if its content is not an integer """

        if self.size_entry.get() == "":
            self.size_entry.state(["invalid"])
        else:
            try:
                if int(self.size_entry.get()) <= 0:
                    self.size_entry.state(["invalid"])
                else:
                    self.size_entry.state(["!invalid"])
            except ValueError:
                self.size_entry.state(["invalid"])

    def validate_path(self, *_):
        """ This method invalidate the entry if its content is not an existing path """

        # if path is empty or incorrect
        if self.save_path_entry.get() == "" or not (path.exists(self.save_path_entry.get())):
            self.save_path_entry.state(["invalid"])

    @staticmethod
    def callback_error(*args):
        # Build the error message
        message = 'Generic error:\n\n'
        message += format_exc()

        # Also log the error to a file
        # TODO

        # Show the error to the user
        messagebox.showerror('Error', message)

    @staticmethod
    def error(message, exception):
        # Build the error message
        if exception is not None:
            message += '\n\n'
            message += format_exc()

        # Also log the error to a file
        # TODO

        # Show the error to the user
        messagebox.showerror('Error', message)

    def center_window(self):
        """ Centers the window on the screen based on screen size """

        win_width, win_height = self.window.winfo_width(), self.window.winfo_height()
        screen_width = int((self.window.winfo_screenwidth() - win_width) / 2)
        screen_height = int((self.window.winfo_screenheight() - win_height) / 2)
        self.window.geometry(f"{win_width}x{win_height}+{screen_width}+{screen_height}")

    def update_entries(self):
        """ Updates entries with default parameters """

        self.until_entry.delete(0, END)
        self.until_entry.insert(0, date.today() - timedelta(days=7))

    def parameters_verification(self):
        """ Verifies that all mandatory parameters are filled """

        save_path = self.save_path_entry.get()
        if save_path == '':
            messagebox.showerror(title="Missing parameter", message="You must select a save "
                                                                    "directory")
            return False

        if not (path.exists(save_path)):
            messagebox.showerror(title="Wrong path", message="You must select a valid save path")
            return False

        try:
            self.size.get()
        except Exception as e:
            self.error('Generic error', e)

            return False

        if self.size.get() <= 0:
            messagebox.showerror(title="Value error", message="We expect a positive number "
                                                              "of results")
            return False

        return True

    def search(self):
        """ Send search parameters to API bridge """

        if self.parameters_verification():
            query = self.query_entry.get("1.0", "end-1c")
            num = self.size.get()
            lan = get_dict_key(self.options, self.language.get())
            res_type = self.result_type_var.get()
            save_path = self.save_path_entry.get()

            print(query, num, lan, res_type, save_path)
            test_api(query, save_path, num, lan, res_type)

    def update_path(self):
        """ Update path entry with user choice """

        save_path = filedialog.askdirectory()
        self.save_path_entry.delete(0, END)  # Remove current text in entry
        self.save_path_entry.insert(0, save_path)  # Insert the 'path'

    def start(self):
        """ Display Tkinter window """

        self.update_entries()  # Updates entries with saved or default values
        self.window.mainloop()
