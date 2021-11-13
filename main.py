import datetime
import os.path
import platform

import pandas as pd

import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table

from header import gen_header_table
from body import gen_body_table
from footer import gen_footer_table


class TimeReport():

    def __init__(self, gui):
        self.gui = gui
        self.df_coach = pd.DataFrame()
        self.df_beginnerluft = pd.DataFrame()
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.date_ranges = None
        self.output_matrix = []
        self.month_selection = []
        self.error = False

        self._get_data()

        if not self.error:
            self._filter_df()
            self._determine_date_range()

    def _get_data(self):

        # get times of coachings conducted by BeginnerLuft
        try:
            if platform.system() == "Darwin":  # MAC
                self.df_coach = pd.read_excel(self.gui.file_ze_coach, sheet_name="Zeiterfassung")
            else:
                if int(pd.__version__[2:4]) < 21:
                    self.df_coach = pd.read_excel(self.gui.file_ze_coach, sheetname="Zeiterfassung")
                else:
                    self.df_coach = pd.read_excel(self.gui.file_ze_coach, sheet_name="Zeiterfassung")
            self.df_coach.dropna(how="all", inplace=True)
            self.df_coach = self.df_coach[["Datum", "Von", "Bis", "UE", "Kommentar bei Terminabsage"]]
        except FileNotFoundError as err:
            print(err)
            pass
        except Exception as err:
            print(err)
            raise Exception

        try:
            if platform.system() == "Darwin":  # MAC
                self.df_beginnerluft = pd.read_excel(self.gui.file_ze_coach, sheet_name="Zeiterfassung")
            else:
                if int(pd.__version__[2:4]) < 21:
                    self.df_beginnerluft = pd.read_excel(self.gui.file_ze_beginnerluft, sheetname="Zeiterfassung")
                else:
                    self.df_beginnerluft = pd.read_excel(self.gui.file_ze_beginnerluft, sheet_name="Zeiterfassung")
            self.df_beginnerluft.dropna(how="all", inplace=True)
            self.df_beginnerluft = self.df_beginnerluft[["Datum", "Von", "Bis", "UE", "Kommentar bei Terminabsage"]]
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print(err)
            raise Exception

        print(self.df_coach)

        # rename columns
        for df in [self.df_coach, self.df_beginnerluft]:
            df.rename(columns={"Kommentar bei Terminabsage": "Kommentar"}, inplace=True)

        try:
            # concatenate the two data frames
            self.df = pd.concat([self.df_beginnerluft, self.df_coach], ignore_index=True)

            # sort dataframe by date
            self.df.sort_values(by=["Datum"], inplace=True)

            self.df["UE"] = self.df["UE"].fillna(0)  # fill UE with zero if cell is empty
            self.df = self.df.fillna("")
            self.filtered_df = self.df.copy()

        except Exception as err:
            print(err)
            self.error = True

    def filter_df(self, months):

        # filter dataframe for specific date range and update output matrix
        self._filter_df(month_selection=months)
        self._determine_date_range()
        # self._create_df_matrix()

    def _filter_df(self, month_selection="all"):

        # filter dataframe for specific date range
        # self.df["Datum"] = pd.to_datetime(self.df["Datum"])
        if month_selection != "all":
            self.filtered_df = self.df[self.df["Datum"].dt.month.isin(month_selection)]

    def _determine_date_range(self):

        if not self.filtered_df.empty:
            # locale.setlocale(locale.LC_TIME, locale.normalize("de"))  # does not work
            first_date = datetime.datetime.strftime(min(self.filtered_df["Datum"]), "%m/%Y")
            last_date = datetime.datetime.strftime(max(self.filtered_df["Datum"]), "%m/%Y")
            date_range = [first_date, last_date]
            self.date_ranges = date_range

    def _create_df_matrix(self):
        sum_ues = "{:.0f}".format(self.filtered_df["UE"].sum())
        self.filtered_df.loc[:, 'Datum'] = self.filtered_df['Datum'].apply(lambda x: x.strftime("%d.%m.%y"))
        self.filtered_df.loc[:, 'Von'] = self.filtered_df['Von'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
        self.filtered_df.loc[:, 'Bis'] = self.filtered_df['Bis'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
        self.filtered_df.loc[:, 'UE'] = self.filtered_df['UE'].apply(lambda x: "{:.0f}".format(x))


        matrix = self.filtered_df.values.tolist()
        matrix.insert(0, self.filtered_df.columns)  # header of dataframe
        matrix.append(["", "", "", sum_ues, ""])

        # ensure that matrix always has the same length and is printed from top to bottom (workaround)
        for i in range(28 - len(matrix)):
            matrix.append(["", "", "", "", ""])

        self.output_matrix = matrix

    def create_report(self, path):

        try:
            # filename = f"BeginnerLuft Zeiterfassung {self.gui.participant_name}.pdf"
            # path = os.path.join(output_directory, filename)
            pdf = canvas.Canvas(path, pagesize=A4)
            pdf.setTitle("BeginnerLuft Zeiterfassung")

            width, height = A4  # A$ is a tuple with two values (width, height)
            height_list = [
                0.15 * height,  # header
                0.80 * height,  # body
                0.05 * height  # footer
                ]

            # create output matrix
            self._create_df_matrix()

            main_table = Table([
                [gen_header_table(width=width, height=height_list[0])],
                [gen_body_table(width=width, height=height_list[1], data=self.output_matrix,
                                training_name=self.gui.training_name, training_nr=self.gui.training_nr,
                                participant_name=self.gui.participant_name, avgs_nr=self.gui.avgs_nr,
                                time_period=self.gui.time_period, date_ranges=self.date_ranges)],
                [gen_footer_table(width=width, height=height_list[2])]
            ],
                colWidths=width,
                rowHeights=height_list,
            )

            main_table.setStyle([
                # ("GRID", (0,0), (-1, -1), 1, "red"),  # a border
                ("LEFTPADDING", (0, 0), (0, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, -2), (-1, -2), 20),
                ("LINEBELOW", (0,1), (-1,1), 1, "grey"),
            ])
            main_table.wrapOn(pdf, 0, 0)
            main_table.drawOn(pdf, 0, 0)

            pdf.showPage()
            pdf.save()

            return True

        except Exception as err:
            return False

