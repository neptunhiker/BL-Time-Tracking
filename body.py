import calendar
import datetime
import pandas as pd
from reportlab.platypus import Table, Image
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

def gen_body_table(width, height, data, training_name, training_nr, participant_name, avgs_nr, time_period, date_ranges):

    participant_name = participant_name
    width_list = [
        0.1 * width,
        0.8 * width,
        0.1 * width,
        ]

    height_list = [
        0.15 * height,
        0.67 * height,
        0.08 * height,
        0.10 * height,
        ]
    res = Table([
        ["", _gen_meta_data(width=width_list[1], height=height_list[3],
                            participant_name=participant_name, training_name=training_name, training_nr=training_nr,
                            avgs_nr=avgs_nr, time_period=time_period, date_ranges=date_ranges), ""],
        ["", _gen_times_table(width=width_list[1], height=height_list[1], data=data), ""],
        ["", _gen_confirmation_text(training_name=training_name, participant_name=participant_name,
                                    date_ranges=date_ranges), ""],
        ["", _gen_signature_table(width=width_list[1], height=height_list[3], participant_name=participant_name), ""],
    ],
        colWidths=width_list,
        rowHeights=height_list
    )

    color = "#FFFF00"
    left_padding = 0

    res.setStyle([
        # ("GRID", (0, 0), (-1, -1), 1, "red"),
        # ("LINEABOVE", (1, 0), (1, 0), 1, color),
        # ("LINEBELOW", (1, 0), (1,-1), 1, "purple"),
        ("LEFTPADDING", (1, 0), (1, 3), left_padding),
        # ("BACKGROUND", (0, 0), (-1, -1), color),
        # ("TEXTCOLOR", (0, 0), (-1, -1), "white"),
        # ("ALIGN", (0, 0), (1, 1), "CENTER"),  # horizontal
        # ("VALIGN", (0, 0), (1, 1), "MIDDLE"),
        # ("LEFTPADDING", (-1, 0), (-1, 0), -width_list[1] + 35),  # unit is points
        # ("FONTSIZE", (2,0), (2,0), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, -2), (-1, -2), 20),
        ("TOPPADDING", (0, 1), (-1, 1), 200),
    ])

    return res


def _gen_meta_data(width, height, participant_name, training_name, training_nr, avgs_nr, time_period, date_ranges):

    # month_names = {}
    # month_names[1] = "Januar"
    # month_names[2] = "Februar"
    # month_names[3] = "März"
    # month_names[4] = "April"
    # month_names[5] = "Mai"
    # month_names[6] = "Juni"
    # month_names[7] = "Juli"
    # month_names[8] = "August"
    # month_names[9] = "September"
    # month_names[10] = "Oktober"
    # month_names[11] = "November"
    # month_names[12] = "Dezember"

    header = "Anwesenheitsliste"
    # min_month = date_ranges[0][0:2]
    # min_year = date_ranges[0][-4:]
    # max_month = date_ranges[1][0:2]
    # max_year = date_ranges[1][-4:]
    # min_month_german = month_names[int(min_month)][0:3]
    # max_month_german = month_names[int(max_month)][0:3]
    #
    # if min_year == max_year:
    #     header = f"{header} {min_month_german} bis {max_month_german} {max_year}"
    # else:
    #     header = f"{header} {min_month_german} {min_year} bis {max_month_german} {max_year}"

    # res = Table([
    #     [header],
    #     [f"Maßnahme: {training_name}"],
    #     [f"Maßnahmennummer: {training_nr}"],
    #     [f"Teilnehmer:in {participant_name}"]
    # ])

    width_list = [
        0.5 * width,
        0.4 * width,
        0.1 * width
        ]

    res = Table([
        [header, ""],
        [f"Teilnehmer:in {participant_name}", f"Maßnahme: {training_name}", ""],
        [f"AVGS-Gutscheinnummer: {avgs_nr}", f"Maßnahmennummer: {training_nr}", ""],
        [f"Bewilligungszeitraum: {time_period}", "", ""]
    ],
        rowHeights=height / 3,
        colWidths=width_list
    )

    res.setStyle([
        # ("GRID", (0, 0), (-1, -1), 1, "red"),
        ("FONTSIZE", (0,0), (0,0), 16),
        ("BOTTOMPADDING", (0, 0), (0, 0), 14)
    ])

    return res

def _gen_times_table(width, height, data):

    width_list = [
        0.15 * width,
        0.15 * width,
        0.15 * width,
        0.15 * width,
        0.4 * width,
        ]

    row_height = height / len(data) * 0.9

    res = Table(
        data,
        colWidths=width_list,
        rowHeights=row_height
    )

    res.setStyle([
        # ("GRID", (0,0), (-1,-1), 1, "red"),
        # ("TEXTCOLOR", (0,0), (-1,0), "red"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("LINEBELOW", (0, 0), (-1, 0), 1, "black"),
        # ("LINEBELOW", (0, -2), (-1, -2), 1, "black"),
        ("ALIGN", (0, 0), (3, -1), "CENTER"),
    ])
    return res

def _gen_confirmation_text(training_name, participant_name, date_ranges):

    # format time period
    if date_ranges[0] == date_ranges[1]:
        time_period = f"{date_ranges[0]}"
    else:
        time_period = f"{date_ranges[0]} bis {date_ranges[1]}"


    para_list = []
    para01_style = ParagraphStyle(name="para01")
    para01_style.spaceAfter = 15
    para01_style.textColor = "green"
    para01 = Paragraph("""
    <b>
    This page tests out a number of attributes of the paraStyle tag. This paragraph is in a
    style we have called "style1". It should be a normal paragraph, set in Courier 12 pt. It
    should be a normal paragraph, set in Courier (not bold).
    </b>
    """, para01_style)

    para02_style = ParagraphStyle(name="para02")
    para02 = Paragraph(f"""
    <i>
    Hiermit bestätige ich, {participant_name}, dass ich im Rahmen der Maßnahme '{training_name}' 
    der <b>BeginnerLuft gGmbH</b> an den oben genannten Terminen teilgenommen habe.
    </i>
    """, para02_style)

    # para_list.append(para01)
    para_list.append(para02)


    return para_list

def _gen_signature_table(width, height, participant_name):

    width_list = [
        0.4 * width,
        0.2 * width,
        0.4 * width
    ]

    # img_path = "resources/Vanguard.png"
    # img_width = width_list[0] * 0.6
    # img_height = height * 0.5
    # img = Image(filename=img_path, width=img_width, height=img_height, kind="proportional")

    res = Table([
        ["_" * 30, "", "_" * 30],
        ["BeginnerLuft", "", participant_name],
    ],
        rowHeights=height / 5,
        colWidths=width_list,
    )

    res.setStyle([
        # ("GRID", (0,0), (-1,-1), 1, "blue"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ])



    return res