import datetime
import os.path

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
        self.date_ranges = None
        self.output_matrix = []

        self._get_data()
        self._filter_df()
        self._determine_date_range()
        self._create_df_matrix()


    def _get_data(self):

        # get times of coachings conducted by BeginnerLuft
        self.df_coach = pd.read_excel(self.gui.file_ze_coach)
        self.df_beginnerluft =pd.read_excel(self.gui.file_ze_beginnerluft)

        # concatenate the two data frames
        self.df = pd.concat([self.df_beginnerluft, self.df_coach], ignore_index=True)

        # sort dataframe by date
        self.df.sort_values(by=["Datum"], inplace=True)

        self.df["UE"] = self.df["UE"].fillna(0)  # fill UE with zero if cell is empty
        self.df = self.df.fillna("")


    def _filter_df(self, month="all"):

        # filter dataframe for specific date range
        if month != "all":
            self.df = self.df[self.df["Datum"].dt.month == month]

    def _determine_date_range(self):

        # locale.setlocale(locale.LC_TIME, locale.normalize("de"))  # does not work
        first_date = datetime.datetime.strftime(min(self.df["Datum"]), "%m/%Y")
        last_date = datetime.datetime.strftime(max(self.df["Datum"]), "%m/%Y")
        date_range = [first_date, last_date]
        self.date_ranges = date_range

    def _create_df_matrix(self):
        sum_ues = "{:.0f}".format(self.df["UE"].sum())
        self.df['Datum'] = self.df['Datum'].apply(lambda x: x.strftime("%d.%m.%y"))
        self.df['Von'] = self.df['Von'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
        self.df['Bis'] = self.df['Bis'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
        self.df['UE'] = self.df['UE'].apply(lambda x: "{:.0f}".format(x))


        matrix = self.df.values.tolist()
        matrix.insert(0, self.df.columns)  # header of dataframe
        matrix.append(["", "", "", sum_ues, ""])

        # ensure that matrix always has the same length and is printed from top to bottom (workaround)
        for i in range(24 - len(matrix)):
            matrix.append(["", "", "", "", ""])

        self.output_matrix = matrix

    def create_report(self, output_directory):

        try:
            filename = f"BeginnerLuft Zeiterfassung {self.gui.participant_name}.pdf"
            path = os.path.join(output_directory, filename)
            pdf = canvas.Canvas(path, pagesize=A4)
            pdf.setTitle(filename)

            width, height = A4  # A$ is a tuple with two values (width, height)
            height_list = [
                0.15 * height,  # header
                0.80 * height,  # body
                0.05 * height  # footer
                ]

            main_table = Table([
                [gen_header_table(width=width, height=height_list[0])],
                [gen_body_table(width=width, height=height_list[1], data=self.output_matrix,
                                training_name=self.gui.training_name, training_nr=self.gui.training_nr,
                                participant_name=self.gui.participant_name, month="all", date_ranges=self.date_ranges)],
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

