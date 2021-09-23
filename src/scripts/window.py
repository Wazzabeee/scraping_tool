from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog


class ScraperWindow:

    def __init__(self):
        """Tkinter objects definitions"""
        self.window = Tk()
        self.window.withdraw()
        self.window.title("Scraping tool")

        # Search type selection
        self.search_type_frame = Labelframe(self.window, text="Search type", borderwidth=1, padding="3 3 12 12")
        self.search_type_frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10)

        self.search_type_var = IntVar(None, 1)

        self.seven_day_check = Radiobutton(self.search_type_frame, text="7 Days search", variable=self.search_type_var,
                                           value=1).grid(row=1, column=1, sticky=S, padx=10, pady=10)
        self.thirty_day_check = Radiobutton(self.search_type_frame, text="30 Days search",
                                            variable=self.search_type_var,
                                            value=2).grid(row=1, column=2, sticky=S, padx=10, pady=10 )
        self.full_archive_check = Radiobutton(self.search_type_frame, text="Full archive search",
                                              variable=self.search_type_var, value=3).grid(row=1, column=3, sticky=S, padx=10, pady=10)

        # Seven days search form
        self.form_frame = Labelframe(self.window, text="Search form", borderwidth=1, padding="3 3 12 12")
        self.form_frame.grid(column=0, row=1, sticky=(N, W, E, S), padx=10, pady=10)

        options = {
            'fr': 'French',
            'en': 'English',
            'es': 'Spanish',
            'de': 'German'
        }
        self.language_label = Label(self.form_frame, text="Search language").grid(row=0, column=0, padx=5, pady=5)
        self.language = StringVar()
        self.language_drop = OptionMenu(self.form_frame, self.language, *options.values())
        self.language_drop.grid(column=1, row=0, padx=20, pady=20)

        self.date_label = Label(self.form_frame, text="Search until").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.date = StringVar()
        self.until_entry = Entry(self.form_frame, textvariable=self.date)
        self.until_entry.insert(-1, 'YYYY-MM-DD')
        self.until_entry.grid(row=1, column=1, sticky=W, padx=10, pady=10)

        self.geocode_label = Label(self.form_frame, text="Results near").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.geocode = StringVar()
        self.geocode_entry = Entry(self.form_frame, textvariable=self.geocode)
        self.geocode_entry.insert(-1, 'XXX,YYY,ZZ')
        self.geocode_entry.grid(row=2, column=1, sticky=W, padx=10, pady=10)

        self.size_label = Label(self.form_frame, text="Number of results").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.size = IntVar()
        self.size_entry = Entry(self.form_frame, textvariable=self.size)
        self.size_entry.grid(row=3, column=1, sticky=W, padx=10, pady=10)

        self.result_type_label = Label(self.form_frame, text="Result type").grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.result_type_frame = LabelFrame(self.form_frame)
        self.result_type_var = IntVar(None, 1)
        self.mixed_check = Radiobutton(self.result_type_frame, text="Mixed", variable=self.result_type_var,
                                       value=1)

        self.recent_check = Radiobutton(self.result_type_frame, text="Recent", variable=self.result_type_var,
                                        value=2)

        self.popular_check = Radiobutton(self.result_type_frame, text="Popular", variable=self.result_type_var,
                                         value=3)

        self.result_type_frame.grid(row=4, column=1, pady=10, padx=10)
        self.mixed_check.pack(expand=True, side=LEFT)
        self.recent_check.pack(expand=True, side=LEFT)
        self.popular_check.pack(expand=True, side=LEFT)

        self.query_label = Label(self.form_frame, text="Query").grid(row=5, column=0, sticky=W, padx=5, pady=5)
        self.query_entry = Text(self.form_frame, width="50", height="5")
        self.query_entry.grid(row=5, column=1, sticky=W, padx=10, pady=10)

        # Seven days search form
        self.save_frame = Labelframe(self.window, text="Save", borderwidth=1, padding="3 3 12 12")
        self.save_frame.grid(column=0, row=2, sticky=(N, W, E, S), padx=10, pady=10)

        self.save_path_label = Label(self.save_frame, text="Save directory").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.save_path_entry = Entry(self.save_frame, text="", width=55)
        self.save_path_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.browse_button = Button(self.save_frame, text="Browse", command=self.update_path).grid(row=0, column=2, sticky=W, padx=5, pady=5)

        self.save_type_label = Label(self.save_frame, text="Save format").grid(row=1, column=0, sticky=W, padx=5,
                                                                                 pady=5)
        self.save_type_frame = LabelFrame(self.save_frame)
        self.save_type_var = IntVar(None, 1)

        self.json_check = Radiobutton(self.save_type_frame, text="JSON", variable=self.save_type_var,
                                       value=1)

        self.csv_check = Radiobutton(self.save_type_frame, text="CSV", variable=self.save_type_var,
                                        value=2)

        self.save_type_frame.grid(row=1, column=1, pady=10, padx=10)
        self.json_check.pack(expand=True, side=LEFT)
        self.csv_check.pack(expand=True, side=LEFT)

        self.search_button = Button(self.window, text="Search", command=self.search).grid(row=3, column=0,
                                                                                                   sticky=N, padx=5,
                                                                                                   pady=5)

        # Center window on screen
        self.window.update()
        self.center_window()
        self.window.deiconify()
        self.window.iconbitmap("../images/cobweb.ico")

    def center_window(self):
        w, h = self.window.winfo_width(), self.window.winfo_height()
        x = int((self.window.winfo_screenwidth() - w) / 2)
        y = int((self.window.winfo_screenheight() - h) / 2)
        self.window.geometry(f'{w}x{h}+{x}+{y}')

    def search(self):
        self.form_frame.grid_forget()

    def update_path(self):
        path = filedialog.askdirectory()
        self.save_path_entry.delete(0, END)  # Remove current text in entry
        self.save_path_entry.insert(0, path)  # Insert the 'path'

    def start(self):
        # Run the main loop
        self.window.mainloop()
