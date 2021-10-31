import datetime
import locale
import pandas as pd

import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table

from header import gen_header_table
from body import gen_body_table
from footer import gen_footer_table


def get_data(month="all"):

    # get times of coachings conducted by BeginnerLuft
    df_bl = pd.read_excel(r"resources/timetable BL.xlsx")

    # get times of coachings conducted by coach
    df_coach = pd.read_excel(r"resources/timetable.xlsx")

    # concatenate the two data frames
    df = pd.concat([df_bl, df_coach], ignore_index=True)

    # sort dataframe by date
    df.sort_values(by=["Datum"], inplace=True)

    df["UE"] = df["UE"].fillna(0)  # fill UE with zero if cell is empty
    df = df.fillna("")

    # filter dataframe for specific date range
    if month != "all":
        df = df[df["Datum"].dt.month == month]

    # locale.setlocale(locale.LC_TIME, locale.normalize("de"))  # does not work
    first_date = datetime.datetime.strftime(min(df["Datum"]), "%m/%Y")
    last_date = datetime.datetime.strftime(max(df["Datum"]), "%m/%Y")
    date_range = [first_date, last_date]
    sum_ues = "{:.0f}".format(df["UE"].sum())
    df['Datum'] = df['Datum'].apply(lambda x: x.strftime("%d.%m.%y"))
    df['Von'] = df['Von'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
    df['Bis'] = df['Bis'].apply(lambda x: x.strftime("%H:%M") if isinstance(x, datetime.datetime) else x)
    df['UE'] = df['UE'].apply(lambda x: "{:.0f}".format(x))
    matrix = df.values.tolist()
    matrix.insert(0, df.columns)  # header of dataframe
    matrix.append(["", "", "", sum_ues, ""])

    # ensure that matrix always has the same length and is printed from top to bottom (workaround)
    for i in range(24 - len(matrix)):
        matrix.append(["", "", "", "", ""])

    return matrix, date_range


training_name = "Individuelles Berufscoaching"
training_nr = "962/400/20"
participant_name = "Emmad Sanib"
month = "all"

pdf = canvas.Canvas("report.pdf", pagesize=A4)
pdf.setTitle("Vanguard Report")

width, height = A4  # A$ is a tuple with two values (width, height)
height_list = [
    0.15 * height,  # header
    0.80 * height,  # body
    0.05 * height  # footer
]

# get data
data, date_ranges = get_data(month=month)

main_table = Table([
    [gen_header_table(width=width, height=height_list[0])],
    [gen_body_table(width=width, height=height_list[1], data=data, training_name=training_name,
                    training_nr=training_nr, participant_name=participant_name, month=month, date_ranges=date_ranges)],
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




