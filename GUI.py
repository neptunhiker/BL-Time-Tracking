import os
import tkinter as tk
from tkinter import ttk

from main_menu import MainMenu


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
        self.style.configure("BackForw.TLabel", background="yellow", foreground="black", font=("Times New Roman", 10, "bold"))
        self.style.configure("Inactive.Nav.TLabel", justify="CENTER", background="lightgrey", foreground="grey",
                             font=("Times New Roman", 12))
        self.style.configure("Data.TLabel", justify="CENTER", background="yellow", foreground="black",
                             font=("Times New Roman", 12))
        self.style.configure("Timetracking.TLabel", anchor="CENTER", background="yellow",
                             font=("Times New Roman", 20, "bold"))
        self.style.configure("Data.TEntry", width=60)
        self.geometry("500x300")

        self.participant_name = ""
        self.training_name = "Individuelles Berufscoaching"
        self.training_nr = "962/400/20"

        self.ent_name = None
        self.ent_t_name = None
        self.ent_t_nr = None

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
        self.lbl_title.grid(row=0, column=0, sticky="nsew", padx=50, pady=100)
        self.lbl_title.bind("<Button-1>", func=self.create_menu_functions)

    def create_menu_functions(self, event):
        self.active_frame.destroy()
        self.nav_frame.destroy()

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_rowconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(0, weight=1)
        lbl = ttk.Label(self.active_frame, text="Zeiterfassung starten!", style="Timetracking.TLabel")
        lbl.grid(row=0, column=0, sticky="nsew")
        lbl.bind("<Button-1>", func=self.create_menu_data)

    def create_menu_data(self, event):

        self.nav_frame.destroy()
        self.active_frame.destroy()

        format_choice = [1, 0, 0, 0, 0]
        self.create_nav(format_choice)

        self.active_frame = ttk.Frame(self, style="Intro.TFrame")
        self.active_frame.grid(row=1, column=0, sticky="nsew")
        self.active_frame.grid_columnconfigure(0, weight=1)
        self.active_frame.grid_columnconfigure(1, weight=1)
        for i in range(3):
            self.active_frame.grid_rowconfigure(i, weight=1)

        lbl_name = ttk.Label(self.active_frame, text="Teilnehmer:in", style="Data.TLabel")
        lbl_name.grid(row=0, column=0, sticky="se")
        self.ent_name = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        self.set_entry_text(self.ent_name, self.participant_name)
        self.ent_name.grid(row=0, column=1, sticky="sw", padx=(20,0))


        lbl_training_name = ttk.Label(self.active_frame, text="Maßnahmenbezeichnung", style="Data.TLabel")
        lbl_training_name.grid(row=1, column=0, sticky="e")
        self.ent_t_name = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        self.set_entry_text(self.ent_t_name, self.training_name)
        self.ent_t_name.grid(row=1, column=1, sticky="w", padx=(20,0))

        lbl_training_nr = ttk.Label(self.active_frame, text="Maßnahmennummer", style="Data.TLabel")
        lbl_training_nr.grid(row=2, column=0, sticky="ne")
        self.ent_t_nr = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        self.set_entry_text(self.ent_t_nr, self.training_nr)
        self.ent_t_nr.grid(row=2, column=1, sticky="nw", padx=(20,0))

        # back and forward button
        self.create_button_back(row=3, collection_function=self.collection_data, nav_function=self.create_menu_functions)
        self.create_button_forward(row=3, column=1, collection_function=self.collection_data, nav_function=self.create_menu_ze_coach)

    def collection_data(self, event):
        self.participant_name = self.ent_name.get()
        self.training_name = self.ent_t_name.get()
        self.training_nr = self.ent_t_nr.get()
        print("-"*20)
        print(self.participant_name)
        print(self.training_nr)
        print(self.training_name)
        print("-"*20)

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
        #
        # lbl_name = ttk.Label(self.active_frame, text="Teilnehmer:in", style="Data.TLabel")
        # lbl_name.grid(row=0, column=0, sticky="se")
        # ent_name = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        # ent_name.grid(row=0, column=1, sticky="sw", padx=(20,0))
        #
        #
        # lbl_training_name = ttk.Label(self.active_frame, text="Maßnahmenbezeichnung", style="Data.TLabel")
        # lbl_training_name.grid(row=1, column=0, sticky="e")
        # ent_t_name = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        # self.set_entry_text(ent_t_name, "Individuelles Berufscoaching")
        # ent_t_name.grid(row=1, column=1, sticky="w", padx=(20,0))
        #
        # lbl_training_nr = ttk.Label(self.active_frame, text="Maßnahmennummer", style="Data.TLabel")
        # lbl_training_nr.grid(row=2, column=0, sticky="ne")
        # ent_t_nr = ttk.Entry(self.active_frame, style="Data.TEntry", width=30)
        # self.set_entry_text(ent_t_nr, "962/400/20")
        # ent_t_nr.grid(row=2, column=1, sticky="nw", padx=(20,0))

        # back and forward button
        self.create_button_back(row=3, collection_function=self.collection_placeholder,
                                nav_function=self.create_menu_data)
        self.create_button_forward(row=3, column=1, collection_function=self.collection_placeholder,
                                   nav_function=self.create_menu_functions)

    def create_button_back(self, row, collection_function, nav_function):
        lbl_back = ttk.Label(self.active_frame, text="<<< Zurück", style="BackForw.TLabel")
        lbl_back.grid(row=row, column=0, sticky="sw")
        lbl_back.bind("<Button-1>", func=collection_function, add="+")
        lbl_back.bind("<Button-1>", func=nav_function, add="+")

    def create_button_forward(self, row, column, collection_function, nav_function):
        lbl_forward = ttk.Label(self.active_frame, text="Vor >>>", style="BackForw.TLabel")
        lbl_forward.grid(row=row, column=column, sticky="se")
        lbl_forward.bind("<Button-1>", func=collection_function, add="+")
        lbl_forward.bind("<Button-1>", func=nav_function, add="+")

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

        lbl_timeperiod = ttk.Label(self.nav_frame, text="Zeitraum", style=styles[format_choice[3]])
        lbl_timeperiod.grid(row=0, column=3, sticky="n", padx=10, pady=5)

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
