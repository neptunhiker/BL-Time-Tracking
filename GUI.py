import datetime
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

from main_menu import MainMenu
from main import TimeReport


class BeginnerLuftGUI(tk.Tk):

    def __init__(self):
        super(BeginnerLuftGUI, self).__init__()
        self.title("BeginnerLuft")
        self.style = ttk.Style(self)
        self.style.configure("Intro.TFrame", background="yellow")
        self.style.configure("Functions.TFrame", background="red")
        self.style.configure("Nav.TFrame", background="lightgrey")
        self.style.configure("Intro.TLabel", anchor="CENTER", background="yellow",
                             font=("Times New Roman", 36, "bold"))
        self.style.configure("Nav.TLabel", justify="CENTER", background="lightgrey", foreground="black",
                             font=("Times New Roman", 12, "bold"))
        self.style.configure("BackForw.TLabel", background="yellow", foreground="black",
                             font=("Times New Roman", 12, "bold"))
        self.style.configure("Inactive.Nav.TLabel", justify="CENTER", background="lightgrey", foreground="grey",
                             font=("Times New Roman", 12))
        self.style.configure("Data.TLabel", justify="CENTER", background="yellow", foreground="black",
                             font=("Times New Roman", 12, "bold"))
        self.style.configure("ZE.TLabel", anchor="center", background="yellow", foreground="black",
                             font=("Times New Roman", 14, "bold"))
        self.style.configure("Filename.TLabel", anchor="center", background="yellow", foreground="black",
                             font=("Times New Roman", 10, "italic"), justify="center", wraplength=450)
        self.style.configure("Timetracking.TLabel", anchor="CENTER", background="yellow",
                             font=("Times New Roman", 20, "bold"))
        self.style.configure("OverviewHeader.TLabel", background="yellow", foreground="black", justify="left",
                             font=("Times New Roman", 14, "bold"))
        self.style.configure("OverviewLeft.TLabel", background="yellow", foreground="black", justify="right",
                             font=("Times New Roman", 12, "bold"))
        self.style.configure("OverviewRight.TLabel", background="yellow", foreground="black", justify="left",
                             font=("Times New Roman", 12), wraplength=400)
        self.style.configure("Data.TEntry", width=60)
        self.style.configure("TCheckbutton", background="yellow", foreground="black", font=("Times New Roman", 10))

        self.geometry("800x400")

        self.report = None

        self.participant_name = ""
        self.training_name = "Individuelles Berufscoaching"
        self.training_nr = "962/400/20"

        self.ent_name = None
        self.ent_t_name = None
        self.ent_t_nr = None

        self.file_ze_coach = "keine Datei ausgewählt"
        self.file_ze_beginnerluft = "keine Datei ausgewählt"

        self.txt_preview = None
        self.checkbutton_list = []

        self.frame_intro = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame = self.frame_intro
        self.nav_frame = ttk.Frame(self)

        # self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_intro.grid(row=1, column=0, sticky="nsew")
        self.frame_intro.grid_rowconfigure(0, weight=1)
        self.frame_intro.grid_columnconfigure(0, weight=1)

        self.lbl_title = ttk.Label(self.frame_intro, text="BeginnerLuft", style="Intro.TLabel")
        self.lbl_title.grid(row=0, column=0, padx=50, pady=100)
        self.lbl_title.bind("<Button-1>", func=self.create_menu_functions)
        self.lbl_title.bind("<Enter>", func=lambda event, label_widget=self.lbl_title,
                                                   color_change=False: self.lbl_on_enter(event, label_widget, color_change))
        self.lbl_title.bind("<Leave>", func=lambda event, label_widget=self.lbl_title: self.lbl_on_leave(event, label_widget))

    def choose_file(self, event, filetype, textvariable):

        filename = askopenfilename(initialdir=os.getcwd()+"/resources", title="Dateiauswahl")
        if filetype == "coach":
            self.file_ze_coach = filename
            textvariable.set(self.file_ze_coach)
        elif filetype == "beginnerluft":
            self.file_ze_beginnerluft = filename
            textvariable.set(self.file_ze_beginnerluft)
        else:
            pass

    def create_menu_functions(self, event):
        self.active_frame.destroy()
        self.nav_frame.destroy()

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_rowconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(0, weight=1)
        lbl = ttk.Label(self.active_frame, text="Zeiterfassung starten!", style="Timetracking.TLabel")
        lbl.grid(row=0, column=0)
        lbl.bind("<Button-1>", func=self.create_menu_data)
        lbl.bind("<Enter>", func=lambda event, label_widget=lbl: self.lbl_on_enter(event, label_widget))
        lbl.bind("<Leave>", func=lambda event, label_widget=lbl: self.lbl_on_leave(event, label_widget))

    def create_menu_data(self, event):

        self.nav_frame.destroy()
        self.active_frame.destroy()

        format_choice = [1, 0, 0, 0, 0]
        self.create_nav(format_choice)

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_columnconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(1, weight=1)
        for i in range(4):
            self.active_frame.grid_rowconfigure(i, weight=1)

        lbl_header = ttk.Label(self.active_frame, text="Stammdaten", style="OverviewHeader.TLabel")
        lbl_header.grid(row=0, column=1, sticky="sw", padx=(20,0))

        lbl_name = ttk.Label(self.active_frame, text="Teilnehmer:in", style="Data.TLabel")
        lbl_name.grid(row=1, column=0, sticky="se")
        self.ent_name = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        self.set_entry_text(self.ent_name, self.participant_name)
        self.ent_name.grid(row=1, column=1, sticky="sw", padx=(20, 0))

        lbl_training_name = ttk.Label(self.active_frame, text="Maßnahmenbezeichnung", style="Data.TLabel")
        lbl_training_name.grid(row=2, column=0, sticky="e")
        self.ent_t_name = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        self.set_entry_text(self.ent_t_name, self.training_name)
        self.ent_t_name.grid(row=2, column=1, sticky="w", padx=(20, 0))

        lbl_training_nr = ttk.Label(self.active_frame, text="Maßnahmennummer", style="Data.TLabel")
        lbl_training_nr.grid(row=3, column=0, sticky="ne")
        self.ent_t_nr = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        self.set_entry_text(self.ent_t_nr, self.training_nr)
        self.ent_t_nr.grid(row=3, column=1, sticky="nw", padx=(20, 0))

        # back and forward button
        self.create_button_back(row=4, collection_function=self.collection_data,
                                nav_function=self.create_menu_functions)
        self.create_button_forward(row=4, column=1, collection_function=self.collection_data,
                                   nav_function=self.create_menu_ze_coach)

    def collection_data(self, event):
        self.participant_name = self.ent_name.get()
        self.training_name = self.ent_t_name.get()
        self.training_nr = self.ent_t_nr.get()

    def collection_placeholder(self, event):
        print("PLACEHOLDER")

    def create_menu_ze_coach(self, event):

        self.nav_frame.destroy()
        self.active_frame.destroy()

        format_choice = [0, 1, 0, 0, 0]
        self.create_nav(format_choice)

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_columnconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(1, weight=1)
        for i in range(3):
            self.active_frame.grid_rowconfigure(i, weight=1)

        var_ze_coach = tk.StringVar()
        var_ze_coach.set(self.file_ze_coach)
        lbl_file_picker = ttk.Label(self.active_frame, text="Wähle Datei zur Zeiterfassung des Coaches aus",
                                    style="ZE.TLabel")
        lbl_file_picker.grid(row=0, column=0, columnspan=2)
        lbl_file_picker.bind("<Button-1>",
                             func=lambda event, filetype="coach", textvariable=var_ze_coach:
                             self.choose_file(event, filetype, textvariable))
        lbl_file_picker.bind("<Enter>", func=lambda event, label_widget=lbl_file_picker: self.lbl_on_enter(event, label_widget))
        lbl_file_picker.bind("<Leave>", func=lambda event, label_widget=lbl_file_picker: self.lbl_on_leave(event, label_widget))

        lbl_file_name = ttk.Label(self.active_frame, textvariable=var_ze_coach, style="Filename.TLabel")
        lbl_file_name.grid(row=1, column=0, columnspan=2, sticky="ew")

        # to be continued: write function that checks whether selected file is an excel and has a dataframe with
        # the usual columns
        # then create a symbol that shows a checkmark or an x and also an error message
        # back and forward button

        self.create_button_back(row=3, collection_function=self.collection_placeholder,
                                nav_function=self.create_menu_data)
        self.create_button_forward(row=3, column=1, collection_function=self.collection_placeholder,
                                   nav_function=self.create_menu_ze_beginnerluft)

    def create_menu_ze_beginnerluft(self, event):

        self.nav_frame.destroy()
        self.active_frame.destroy()

        format_choice = [0, 0, 1, 0, 0]
        self.create_nav(format_choice)

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_columnconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(1, weight=1)
        for i in range(3):
            self.active_frame.grid_rowconfigure(i, weight=1)

        var_ze_bl = tk.StringVar()
        var_ze_bl.set(self.file_ze_beginnerluft)
        lbl_file_picker = ttk.Label(self.active_frame, text="Wähle Datei zur Zeiterfassung von BeginnerLuft aus",
                                    style="ZE.TLabel")
        lbl_file_picker.grid(row=0, column=0, columnspan=2)
        lbl_file_picker.bind("<Button-1>",
                             func=lambda event, filetype="beginnerluft", textvariable=var_ze_bl:
                             self.choose_file(event, filetype, textvariable))
        lbl_file_picker.bind("<Enter>", func=lambda event, label_widget=lbl_file_picker: self.lbl_on_enter(event, label_widget))
        lbl_file_picker.bind("<Leave>", func=lambda event, label_widget=lbl_file_picker: self.lbl_on_leave(event, label_widget))

        lbl_file_name = ttk.Label(self.active_frame, text="hi", textvariable=var_ze_bl, style="Filename.TLabel")
        lbl_file_name.grid(row=1, column=0, columnspan=2, sticky="ew")

        # to be continued: write function that checks whether selected file is an excel and has a dataframe with
        # the usual columns
        # then create a symbol that shows a checkmark or an x and also an error message
        # back and forward button

        self.create_button_back(row=3, collection_function=self.collection_placeholder,
                                nav_function=self.create_menu_ze_coach)
        self.create_button_forward(row=3, column=1, collection_function=self.collection_placeholder,
                                   nav_function=self.create_menu_data_overview)

    def create_menu_data_overview(self, event):

        self.nav_frame.destroy()
        self.active_frame.destroy()

        format_choice = [0, 0, 0, 1, 0]
        self.create_nav(format_choice)

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_columnconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(1, weight=1)
        for i in range(8):
            self.active_frame.grid_rowconfigure(i, weight=1)

        lbl_overview = ttk.Label(self.active_frame, text="Datenübersicht", style="OverviewHeader.TLabel")

        lbl_name = ttk.Label(self.active_frame, text="Teilnehmer:in", style="OverviewLeft.TLabel")
        lbl_training_name = ttk.Label(self.active_frame, text="Maßnahmenbezeichnung", style="OverviewLeft.TLabel")
        lbl_training_nr = ttk.Label(self.active_frame, text="Maßnahmennummer", style="OverviewLeft.TLabel")
        lbl_file_ze_coach = ttk.Label(self.active_frame, text="Datei ZE Coach", style="OverviewLeft.TLabel")
        lbl_file_ze_bl = ttk.Label(self.active_frame, text="Datei ZE BeginnerLuft", style="OverviewLeft.TLabel")

        left_hand_labels = [lbl_name, lbl_training_name, lbl_training_nr, lbl_file_ze_coach, lbl_file_ze_bl]

        lbl_real_name = ttk.Label(self.active_frame, text=self.participant_name, style="OverviewRight.TLabel")
        lbl_real_training_name = ttk.Label(self.active_frame, text=self.training_name, style="OverviewRight.TLabel")
        lbl_real_training_nr = ttk.Label(self.active_frame, text=self.training_nr, style="OverviewRight.TLabel")
        lbl_real_file_ze_coach = ttk.Label(self.active_frame, text=self.file_ze_coach, style="OverviewRight.TLabel")
        lbl_real_file_ze_bl = ttk.Label(self.active_frame, text=self.file_ze_beginnerluft, style="OverviewRight.TLabel")

        right_hand_labels = [lbl_real_name, lbl_real_training_name, lbl_real_training_nr, lbl_real_file_ze_coach,
                             lbl_real_file_ze_bl]

        lbl_overview.grid(row=0, column=1, sticky="w", pady=(10, 10), padx=(10, 0))

        for i, label in enumerate(left_hand_labels):
            label.grid(row=i + 1, column=0, sticky="ne", padx=(0, 10))

        for i, label in enumerate(right_hand_labels):
            label.grid(row=i + 1, column=1, sticky="nw", padx=(10, 0))


        self.create_button_back(row=8, collection_function=self.collection_placeholder,
                                nav_function=self.create_menu_ze_beginnerluft)
        self.create_button_forward(row=8, column=1, collection_function=self.collection_placeholder,
                                   nav_function=self.create_menu_report)

    def create_menu_report(self, event):

        self.nav_frame.destroy()
        self.active_frame.destroy()

        format_choice = [0, 0, 0, 0, 1]
        self.create_nav(format_choice)

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_columnconfigure(0, weight=10)
        self.active_frame.grid_columnconfigure(1, weight=20)
        self.active_frame.grid_columnconfigure(2, weight=1)
        for i in range(5):
            self.active_frame.grid_rowconfigure(i, weight=1)

        # prepare the report
        self.report = TimeReport(gui=self)

        if not self.report.error:
            lbl_time_period = ttk.Label(self.active_frame, text="Wähle Zeitraum", style="OverviewHeader.TLabel")
            lbl_time_period.grid(row=0, column=0, sticky="nwe", pady=(20,0), padx=(60,0))

            # create and place checkbuttons
            frame_time_period = ttk.Frame(self.active_frame, style="Intro.TFrame")
            frame_time_period.grid(row=1, column=0, sticky = "nsew")
            self.checkbutton_list = self.create_checkbuttons(frame=frame_time_period)
            frame_time_period.grid_columnconfigure(0, weight=1)
            for i, checkbutton in enumerate(self.checkbutton_list):
                frame_time_period.grid_rowconfigure(i, weight=1)
                checkbutton.grid(row=1 + i, column=0, sticky="nw", padx=(60,0))
                checkbutton.var.set(1)  # turns on all checkbuttons

            #  Data preview window
            lbl_preview = ttk.Label(self.active_frame, text="Datenvorschau", style="OverviewHeader.TLabel", anchor=tk.CENTER)
            lbl_preview.grid(row=0, column=1, sticky="nwe", pady=(20,0))
            self.txt_preview = tk.Text(self.active_frame, width=30, height=10)
            self.txt_preview.grid(row=1, column=1, sticky="news", padx=(10,10))

            # insert dataframe content as a preview to user into text field
            self.txt_preview.delete("1.0", tk.END)
            df = self.report.filtered_df.copy()
            df.set_index("Datum", inplace=True)
            self.txt_preview.insert(tk.END, df)

            scrollbar = ttk.Scrollbar(self.active_frame, orient="vertical", command=self.txt_preview.yview)
            scrollbar.grid(row=1, column=2, sticky="ns", padx=(0,10))
            self.txt_preview['yscrollcommand'] = scrollbar.set  #  communicate back to the scrollbar

            lbl_create_report = ttk.Label(self.active_frame, text="Report erstellen!", style="OverviewHeader.TLabel",
                                          anchor=tk.CENTER)
            lbl_create_report.grid(row=3, column=1, sticky="ew", padx=(10, 0))
            lbl_create_report.bind("<Enter>", func=lambda event, label_widget=lbl_create_report: self.lbl_on_enter(event, label_widget))
            lbl_create_report.bind("<Leave>", func=lambda event, label_widget=lbl_create_report: self.lbl_on_leave(event, label_widget))
            lbl_create_report.bind("<Button-1>", self.create_report)

        else:

            lbl_error = ttk.Label(self.active_frame, text="-- Fehler --\n\nBitte Datenübersicht kontrollieren!",
                                  style="OverviewHeader.TLabel", anchor=tk.CENTER, justify="center")
            lbl_error.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.create_button_back(row=4, collection_function=self.collection_placeholder,
                                nav_function=self.create_menu_data_overview)

    def create_report(self, event):

        # directory = askdirectory(initialdir=os.path.join(os.getcwd(), "reports"))
        filename = f"BeginnerLuft Zeiterfassung {self.participant_name}"
        filename = filename.rstrip()
        filename = filename + ".pdf"
        path = asksaveasfilename(title="BeginnerLuft Zeiterfassung", initialdir=os.path.join(os.getcwd(), "reports"),
                                 initialfile=filename, filetypes=(("pdf", "*.pdf"), ))

        print(path)

        # create pdf report
        if not path == "":
            if not self.report.error:
                success = self.report.create_report(path)
            else:
                success = False

            # Success or failure messages of report creation
            if success:
                messagebox.showinfo(title="BeginnerLuft Zeiterfassung",
                                    message=f"Zeiterfassungsreport für {self.participant_name} erstellt. Speicherort:\n\n"
                                            f"{path}")
            else:
                messagebox.showerror(title="BeginnerLuft Zeiterfassung",
                                     message=f"Zeiterfassungsreport für {self.participant_name} konnte nicht erstellt"
                                             f" werden. Bitte kontrollen, ob Zeiterfassungsdateien im richtigen Format "
                                             f"vorliegen. Anschließend die Reporterstellung nochmals starten.")

    def change_preview(self, event, btn):
        # determine selected months
        months = []
        # btn.var.set(1)
        for btn in self.checkbutton_list:
            if (btn.instate(["selected"]) or btn.instate(["active"])) and btn.state() != ('active', 'focus', 'pressed', 'selected', 'hover'):
                months.append(btn.cget("text")[0:2])

        months = [int(month) for month in months]

        # filter dataframe
        self.report.filter_df(months=months)

        # insert dataframe content as a preview to user into text field
        self.txt_preview.delete("1.0", tk.END)

        # insert filtered data only if filtered dataframe has data in it
        if not self.report.filtered_df.empty:
            df = self.report.filtered_df.copy()
            df.set_index("Datum", inplace=True)
            self.txt_preview.insert(tk.END, df)

        scrollbar = ttk.Scrollbar(self.active_frame, orient="vertical", command=self.txt_preview.yview)
        scrollbar.grid(row=1, column=2, sticky="ns", padx=(0,10))
        self.txt_preview['yscrollcommand'] = scrollbar.set  #  communicate back to the scrollbar



    def create_checkbuttons(self, frame):

        # output / return value
        checkbutton_list = []

        # get unique dates
        dates = self.report.df["Datum"].unique()
        formatted_dates = [pd.to_datetime(str(date)).strftime("%m/%Y") for date in dates]

        # keep only unique month/year combinations
        final_dates = set(formatted_dates)

        # sort those combinations
        final_parsed_dates = [datetime.datetime.strptime(date, "%m/%Y") for date in final_dates]
        final_parsed_dates.sort()
        final_formatted_dates = [date.strftime("%m/%Y") for date in final_parsed_dates]

        # create checkbuttons
        for i, date in enumerate(final_formatted_dates):
            var = tk.IntVar()
            cbtn = ttk.Checkbutton(frame, text=date, variable=var, style="TCheckbutton")
            cbtn.bind("<ButtonRelease-1>", lambda event, btn=cbtn: self.change_preview(event, btn=btn))
            cbtn.state(['!alternate'])  # remove alternate selected state
            cbtn.var = var  # attach variable to checkbutton
            checkbutton_list.append(cbtn)

        # var = tk.IntVar()
        # cbtn = ttk.Checkbutton(frame, text="Gesamter Zeitraum", variable=var, style="TCheckbutton")
        # cbtn.bind("<ButtonRelease-1>", lambda event, btn=cbtn: self.change_preview(event, btn=btn))
        # cbtn.state(['!alternate'])  # remove alternate selected state
        # cbtn.var = var  # attach variable to checkbutton
        # checkbutton_list.append(cbtn)

        return checkbutton_list

    def lbl_on_enter(self, event, label_widget, color_change=True):
        if color_change:
            label_widget.configure(foreground="blue", cursor="hand2")
        else:
            label_widget.configure(cursor="hand2")

    def lbl_on_leave(self, event, label_widget):
        label_widget.configure(foreground="black")

    def create_button_back(self, row, collection_function, nav_function):
        lbl_back = ttk.Label(self.active_frame, text="<<< Zurück", style="BackForw.TLabel")
        lbl_back.grid(row=row, column=0, sticky="sw", pady=7, padx=10)
        lbl_back.bind("<Button-1>", func=collection_function, add="+")
        lbl_back.bind("<Button-1>", func=nav_function, add="+")
        lbl_back.bind("<Enter>", func=lambda event, label_widget=lbl_back: self.lbl_on_enter(event, label_widget))
        lbl_back.bind("<Leave>", func=lambda event, label_widget=lbl_back: self.lbl_on_leave(event, label_widget))

    def create_button_forward(self, row, column, collection_function, nav_function):
        lbl_forward = ttk.Label(self.active_frame, text="Vor >>>", style="BackForw.TLabel")
        lbl_forward.grid(row=row, column=column, sticky="se", pady=7, padx=10)
        lbl_forward.bind("<Button-1>", func=collection_function, add="+")
        lbl_forward.bind("<Button-1>", func=nav_function, add="+")
        lbl_forward.bind("<Enter>", func=lambda event, label_widget=lbl_forward: self.lbl_on_enter(event, label_widget))
        lbl_forward.bind("<Leave>", func=lambda event, label_widget=lbl_forward: self.lbl_on_leave(event, label_widget))

    def create_nav(self, format_choice):

        styles = ["Inactive.Nav.TLabel", "Nav.TLabel", ]
        self.nav_frame = ttk.Frame(self, style="Nav.TFrame")
        self.nav_frame.grid(row=0, column=0, sticky="ew")

        lbl_data = ttk.Label(self.nav_frame, text="Daten", style=styles[format_choice[0]])
        lbl_data.grid(row=0, column=0, sticky="n", padx=10, pady=5)

        lbl_tt_coach = ttk.Label(self.nav_frame, text="ZE Coach", style=styles[format_choice[1]])
        lbl_tt_coach.grid(row=0, column=1, sticky="n", padx=10, pady=5)

        lbl_tt_bl = ttk.Label(self.nav_frame, text="ZE BeginnerLuft", style=styles[format_choice[2]])
        lbl_tt_bl.grid(row=0, column=2, sticky="n", padx=10, pady=5)

        lbl_data_overview = ttk.Label(self.nav_frame, text="Datenübersicht", style=styles[format_choice[3]])
        lbl_data_overview.grid(row=0, column=3, sticky="n", padx=10, pady=5)

        lbl_output = ttk.Label(self.nav_frame, text="Report Erstellung", style=styles[format_choice[4]])
        lbl_output.grid(row=0, column=4, sticky="n", padx=10, pady=5)

    def open_new_window(self, event, type):
        if type == "main menu":
            menu = MainMenu()
        elif type == "common data":
            pass

        # path = os.path.join("resources","beginnerluft.png")
        # img = tk.PhotoImage(file=path)
        # lbl = tk.Label(self.frame_intro, image=img)
        # lbl.grid(row=0, column=0)

    def set_entry_text(self, the_widget, text):
        the_widget.delete(0, tk.END)
        the_widget.insert(0, text)


class TopLevel(tk.Toplevel):

    def __init__(self, event):
        super(TopLevel, self).__init__()


if __name__ == '__main__':
    app = BeginnerLuftGUI()
    app.mainloop()
