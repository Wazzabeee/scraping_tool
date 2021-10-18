"""
This module is the GUI for Twitter API
@author : Clément Delteil
"""
import csv
import json
from datetime import date, datetime, timedelta
from os import path, getcwd
from tkinter import (
    Tk,
    ttk,
    filedialog,
    messagebox,
    IntVar,
    StringVar,
    N,
    S,
    E,
    W,
    LEFT,
    Text,
    END,
)
from traceback import format_exc

from data import save_search_settings, save_user_settings
from twitter import api_search, retrieve_tweets_from_users_list
from utils import get_dict_key, separate_int_string, validate_date_format


class ScraperWindow:
    """This class represents the twitter api window"""

    def __init__(self, master):
        """Tkinter UI objects definitions"""

        self.master = master
        self.tab_control = ttk.Notebook(self.master)
        self.frame = ttk.Frame(self.tab_control)
        self.user_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.frame, text="Search")
        self.tab_control.add(self.user_frame, text="User")
        self.tab_control.grid(row=0, column=0, sticky=N + S + W + E)

        self.master.withdraw()
        self.master.title("Scraping tool")

        # Overwrite Tk callback exception to get message on the screen when error occures
        Tk.report_callback_exception = self.callback_error

        """ Search tab UI components """
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
            # self.window,
            self.frame,
            text="Search type",
            borderwidth=1,
            padding="80 3 12 12",
        )
        self.form_frame = ttk.Labelframe(
            self.frame, text="Search form", borderwidth=1, padding="3 3 12 12"
        )
        self.save_frame = ttk.Labelframe(
            self.frame, text="Save", borderwidth=1, padding="3 3 12 12"
        )
        self.result_type_frame = ttk.LabelFrame(self.form_frame, padding="5 0 3 8")
        self.save_type_frame = ttk.Labelframe(self.save_frame, padding="5 0 3 8")

        self.language_drop = ttk.OptionMenu(
            self.form_frame, self.language, self.options["en"], *self.options.values()
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
            value="mixed",
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
            self.save_type_frame, text="JSON", variable=self.save_type_var, value=1
        )
        self.csv_check = ttk.Radiobutton(
            self.save_type_frame,
            text="CSV",
            variable=self.save_type_var,
            value=2,
            state="disable",
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
            state="disable",
        )
        self.full_archive_check = ttk.Radiobutton(
            self.search_type_frame,
            text="Full archive search",
            variable=self.search_type_var,
            value=3,
            state="disable",
        )

        self.browse_button = ttk.Button(
            self.save_frame,
            text="Browse",
            style="Accent.TButton",
            command=lambda: self.update_path("first"),
        )
        self.search_button = ttk.Button(
            self.frame, text="Search", style="Accent.TButton", command=self.search
        )

        # Placement of search tab UI components
        self.search_type_frame.grid(
            column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10
        )
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

        # User tab UI elements
        self.import_user_frame = ttk.Labelframe(
            self.user_frame,
            text="Import users list",
            borderwidth=1,
            padding="3 3 12 12",
        )

        self.parameters_frame = ttk.Labelframe(
            self.user_frame,
            text="True/False parameters",
            borderwidth=1,
            padding="110 3 12 12",
        )

        self.entries_frame = ttk.LabelFrame(
            self.user_frame,
            text="Optional entries",
            borderwidth=1,
            padding="3 3 12 12 ",
        )

        self.save_frame2 = ttk.Labelframe(
            self.user_frame, text="Save", borderwidth=1, padding="3 3 12 12"
        )

        self.browse_button2 = ttk.Button(
            self.import_user_frame,
            text="Browse",
            style="Accent.TButton",
            command=lambda: self.update_path("second"),
        )

        self.browse_button3 = ttk.Button(
            self.save_frame2,
            text="Browse",
            style="Accent.TButton",
            command=lambda: self.update_path("third"),
        )

        self.search_button2 = ttk.Button(
            self.user_frame,
            text="Search",
            style="Accent.TButton",
            command=self.user_search,
        )

        # Variables linked to user tab components
        self.include_rt = IntVar()
        self.exclude_replies = IntVar()
        self.trim_user = IntVar()
        self.count = IntVar()
        self.since_date = StringVar()
        self.until_date = StringVar()

        self.include_rt_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Include RT",
            variable=self.include_rt,
            onvalue=1,
            offvalue=0,
        )

        self.exclude_replies_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Exclude replies",
            variable=self.exclude_replies,
            onvalue=1,
            offvalue=0,
        )

        self.trim_user_button = ttk.Checkbutton(
            self.parameters_frame,
            text="Only user ID",
            variable=self.trim_user,
            onvalue=1,
            offvalue=0,
        )
        self.save_path_label2 = ttk.Label(self.save_frame2, text="Save directory")
        self.save_path_entry2 = ttk.Entry(self.save_frame2, text="", width=55)
        self.since_date_entry = ttk.Entry(
            self.entries_frame, textvariable=self.since_date
        )
        self.until_date_entry = ttk.Entry(
            self.entries_frame, textvariable=self.until_date
        )
        self.count_entry = ttk.Entry(self.entries_frame, textvariable=self.count)
        self.since_date_label = ttk.Label(self.entries_frame, text="Since")
        self.until_date_label = ttk.Label(self.entries_frame, text="Until")
        self.count_label = ttk.Label(
            self.entries_frame, text="Number of results per page"
        )
        self.import_user_path_label = ttk.Label(
            self.import_user_frame, text="Users list"
        )
        self.import_user_path_entry = ttk.Entry(
            self.import_user_frame, text="", width=55
        )

        # Placement of user tab UI components
        self.import_user_path_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.import_user_path_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.browse_button2.grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.include_rt_button.grid(row=0, column=0, sticky=N, padx=5, pady=5)
        self.exclude_replies_button.grid(row=0, column=1, sticky=N, padx=5, pady=5)
        self.trim_user_button.grid(row=0, column=2, sticky=N, padx=5, pady=5)
        self.count_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.count_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        self.since_date_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.since_date_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.until_date_label.grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.until_date_entry.grid(row=0, column=3, sticky=W, padx=5, pady=5)
        self.import_user_frame.grid(
            column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10
        )
        self.parameters_frame.grid(
            column=0, row=1, sticky=(N, W, E, S), padx=10, pady=10
        )
        self.entries_frame.grid(column=0, row=2, sticky=(N, W, E, S), padx=10, pady=10)
        self.save_frame2.grid(column=0, row=3, sticky=(N, W, E, S), padx=10, pady=10)
        self.save_path_label2.grid(column=0, row=3, sticky=W, padx=5, pady=5)
        self.save_path_entry2.grid(column=1, row=3, sticky=W, padx=5, pady=5)
        self.browse_button3.grid(column=2, row=3, sticky=W, padx=5, pady=5)
        self.search_button2.grid(column=0, row=4, sticky=N, padx=5, pady=5)

        # Make window appear again
        self.master.update()  # Update default or saved values
        self.center_window()  # Center the window on the screen
        self.master.deiconify()
        self.master.iconbitmap("../images/cobweb.ico")  # Add icon to window
        self.bind_them()  # Bind events to objects
        self.update_entries()

    def bind_them(self):
        """This method binds events to Tkinter objects"""

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
        """This method invalidates the entry if its content is not a valid geolocalization"""

        if self.geocode_entry.get() == "":
            self.geocode_entry.state(["invalid"])
            return False

        try:
            geocode = self.geocode_entry.get()
            lat, long, rad = geocode.split(",")
            if not (lat == "" or long == "" or rad == ""):
                lat.replace(".", ",")
                long.replace(".", ",")
                if -90 <= float(lat) <= 90 and -180 <= float(long) <= 180:
                    radius, unit = separate_int_string(rad)
                    if radius.isnumeric() and (
                            str(unit) == "km" or str(unit) == "mi"
                    ):
                        self.geocode_entry.state(["!invalid"])
                        return True
                    self.geocode_entry.state(["invalid"])
                    return False

                self.geocode_entry.state(["invalid"])
                return False

            self.geocode_entry.state(["invalid"])
            return False

        except ValueError:
            self.geocode_entry.state(["invalid"])
            return False

    def validate_date(self, *_):
        """This method invalidates the entry if its content is not a valid date"""

        if self.until_entry.get() == "":
            self.until_entry.state(["invalid"])
            return False

        try:
            datetime.strptime(self.until_entry.get(), "%Y-%m-%d")

            # checks if date is sooner than 7 days from today
            if datetime.strptime(self.until_entry.get(), "%Y-%m-%d") <= (
                    datetime.today() - timedelta(days=8)
            ):
                self.until_entry.state(["invalid"])
                return False

            self.until_entry.state(["!invalid"])
            return True

        except ValueError:
            self.until_entry.state(["invalid"])
            return False

    def validate_int(self, *_):
        """This method invalidates the entry if its content is not an integer"""

        if self.size_entry.get() == "":
            self.size_entry.state(["invalid"])
            return False

        try:
            if int(self.size_entry.get()) <= 0:
                self.size_entry.state(["invalid"])
                return False

            self.size_entry.state(["!invalid"])
            return True

        except ValueError:
            self.size_entry.state(["invalid"])
            return False

    def validate_query(self, *_):
        """This method invalidates the entry if the query is empty"""

        if self.query_entry.get("1.0", "end-1c") == "":
            return False

        return True

    def validate_path(self, *_):
        """This method invalidates the entry if its content is not an existing path"""

        # if path is empty or incorrect
        if self.save_path_entry.get() == "" or not (
                path.exists(self.save_path_entry.get())
        ):
            self.save_path_entry.state(["invalid"])
            return False

        self.save_path_entry.state(["!invalid"])
        return True

    @staticmethod
    def callback_error():
        """ Overrides console callback error to display it on the GUI """
        # Build the error message
        message = "Generic error:\n\n"
        message += format_exc()

        # Show the error to the user
        messagebox.showerror("Error", message)

    @staticmethod
    def error(message, exception):
        """ Overrides error to display it on the GUI """

        # Build the error message
        if exception is not None:
            message += "\n\n"
            message += format_exc()

        # Show the error to the user
        messagebox.showerror("Error", message)

    def center_window(self):
        """Centers the window on the screen based on screen size"""

        win_width, win_height = self.master.winfo_width(), self.master.winfo_height()
        screen_width = int((self.master.winfo_screenwidth() - win_width) / 2)
        screen_height = int((self.master.winfo_screenheight() - win_height) / 2)
        self.master.geometry(f"{win_width}x{win_height}+{screen_width}+{screen_height}")

    def update_entries(self):
        """Updates entries with default parameters"""

        self.size_entry.delete(0, END)

        if path.exists("../settings/search_settings.json"):
            with open("../settings/search_settings.json") as file:
                data = json.load(file)

            for item in data["query_research"]:
                if item["query"] != "":
                    self.query_entry.insert(END, item["query"])
                if item["save_path"] != "":
                    self.save_path_entry.insert(END, item["save_path"])
                if item["geocode"] != "":
                    self.geocode_entry.insert(END, item["geocode"])
                if item["number"] != 0:
                    self.size_entry.insert(END, item["number"])
                if item["until"] != "":
                    self.until_entry.insert(END, item["until"])
                else:
                    self.until_entry.insert(0, date.today() - timedelta(days=7))

                if item["research_type"] != "":
                    self.result_type_var.set(item["research_type"])
                if item["language"] != "":
                    self.language.set(self.options[item["language"]])

        if path.exists("../settings/user_settings.json"):
            with open("../settings/user_settings.json") as file:
                data = json.load(file)

            for item in data["user_research"]:
                if item["users_lists"] != "":
                    self.import_user_path_entry.insert(END, item["users_lists"])
                if item["save_path"] != "":
                    self.save_path_entry2.insert(END, item["save_path"])
                if item["include_rts"] != "":
                    if item["include_rts"]:
                        self.include_rt.set(1)
                if item["exclude_replies"] != "":
                    if item["exclude_replies"]:
                        self.exclude_replies.set(1)
                if item["trim_user_info"] != "":
                    if item["trim_user_info"]:
                        self.trim_user.set(1)
                if item["since"] != "":
                    self.since_date_entry.insert(END, item["since"])
                if item["until"] != "":
                    self.until_date_entry.insert(END, item["until"])
                if int(item["res_per_page"]) != 0:
                    self.count_entry.insert(END, int(item["res_per_page"]))

    def parameters_verification(self):
        """Verifies that all mandatory parameters fron search tab form are filled"""

        until, size, geocode = False, False, False

        if not self.validate_date():  # if date is not valid
            # if user answers no we break
            if not (
                    messagebox.askyesno(
                        title="Invalid parameter",
                        message="The date you've entered "
                        "is "
                        "not valid.\nDo you want to "
                        "proceed anyway ?\nDefault is "
                        "date is 7 days ago.",
                    )
            ):
                return [False]
            # user answers yes we use default value
            until = False
        else:
            until = True

        if not self.validate_geocode():
            if not (
                    messagebox.askyesno(
                        title="Invalid parameter",
                        message="The geocode you've "
                        "entered "
                        "is not valid.\n"
                        "Do you want to "
                        "proceed anyway ?",
                    )
            ):
                return [False]

            geocode = False
        else:
            geocode = True

        if not self.validate_int():
            if not (
                    messagebox.askyesno(
                        title="Invalid parameter",
                        message="You must select a "
                        "positive int number.\n"
                        "Do you "
                        "want to proceed "
                        "anyway ?\n Default is "
                        "10.",
                    )
            ):
                return [False]

            size = False
        else:
            size = True

        if not self.validate_path():
            messagebox.showerror(
                title="Invalid parameter",
                message="You must select a correct " "save " "directory.",
            )
            return [False]

        if not self.validate_query():
            messagebox.showerror(
                title="Invalid parameter", message="You must enter a query."
            )
            return [False]

        return [True, geocode, until, size]

    def user_parameters_verification(self):
        """Verifies that all mandatory parameters fron user tab form are filled"""

        if self.import_user_path_entry.get() != "":
            _, extension = path.splitext(self.import_user_path_entry.get())
            if extension == ".csv":
                try:
                    res = int(self.count.get()) >= 0
                    if not res:
                        messagebox.showinfo(
                            title="Error",
                            message="Count must be greater or " "equal than 0",
                        )
                    else:
                        return True
                except ValueError:
                    messagebox.showinfo(
                        title="Error",
                        message="Count must be greater or equal " "than 0",
                    )
                    return False
            else:
                messagebox.showinfo(
                    title="File extension error",
                    message="You must select a CSV " "file",
                )
        else:
            messagebox.showinfo(
                title="Missing CSV file", message="You must select a CSV file"
            )

        return False

    def user_search(self):
        """Sends user search parameters to API"""

        # We check if all mandatory parameters are filled
        if self.user_parameters_verification():
            count = None
            names = []
            with open(self.import_user_path_entry.get(), newline="") as user_file:
                for row in csv.reader(user_file):
                    names.append(row[0])

            print(names)
            if len(names) >= 1:  # if file is not empty

                # We retrieve all form's values
                exclude_replies = bool(self.exclude_replies.get())
                include_rt = bool(self.include_rt.get())
                only_userid = bool(self.trim_user.get())
                count = self.count.get() if self.count_entry.get() != 0 else None
                if validate_date_format(self.since_date.get()):
                    sincedate = str(self.since_date.get())
                else:
                    sincedate = ""

                if validate_date_format(self.until_date.get()):
                    untildate = str(self.until_date.get())
                else:
                    untildate = ""

                save_path = (
                    self.save_path_entry2.get()
                    if self.save_path_entry2.get() != ""
                    else path.abspath(getcwd())
                )

                if retrieve_tweets_from_users_list(
                        names,
                        save_path,
                        since=sincedate,
                        count=count,
                        until=untildate,
                        trim_user=only_userid,
                        exclude_replies=exclude_replies,
                        include_rts=include_rt,
                ):

                    save_user_settings(
                        self.import_user_path_entry.get(),
                        save_path,
                        include_rt,
                        exclude_replies,
                        only_userid,
                        sincedate,
                        untildate,
                        count,
                    )
                    messagebox.showinfo(
                        title="Success",
                        message="The results have been saved to the "
                        "specified location.",
                    )
                else:
                    messagebox.showerror(
                        titl="Error",
                        message="Something wrong happenned. Pleae "
                        "check API status or query format.",
                    )

    def search(self):
        """Sends search parameters to API bridge"""

        parameters = self.parameters_verification()

        if parameters[0]:
            # We retrieve mandatory parameters
            query = self.query_entry.get("1.0", "end-1c")
            save_path = self.save_path_entry.get()
            res_type = self.result_type_var.get()
            lan = get_dict_key(self.options, self.language.get())

            # We retrieve optional parameters
            geo_code = self.geocode_entry.get() if parameters[1] else ""
            until = self.until_entry.get() if parameters[2] else ""
            num = int(self.size_entry.get()) if parameters[3] else 10

            if api_search(query, save_path, geo_code, num, until, lan, res_type):
                save_search_settings(
                    query, save_path, geo_code, num, until, lan, res_type
                )
                messagebox.showinfo(
                    title="Success",
                    message="The results have been saved to the " "specified location.",
                )
            else:
                messagebox.showerror(
                    titl="Error",
                    message="Something wrong happenned. Pleae "
                    "check API status or query format.",
                )

    def update_path(self, tab):
        """Updates path entry with user choice"""

        if tab == "first":
            save_path = filedialog.askdirectory()
            self.save_path_entry.delete(0, END)  # Remove current text in entry
            self.save_path_entry.insert(0, save_path)  # Insert the 'path'
        elif tab == "second":
            save_path = filedialog.askopenfilename()
            self.import_user_path_entry.delete(0, END)
            self.import_user_path_entry.insert(0, save_path)
        else:
            save_path = filedialog.askdirectory()
            self.save_path_entry2.delete(0, END)
            self.save_path_entry2.insert(0, save_path)

    def start(self):
        """Displays Tkinter window"""

        self.update_entries()  # Updates entries with saved or default values
        self.master.mainloop()
