<<<<<<< HEAD


from reportlab.platypus import Table
from reportlab.lib import colors


def gen_footer_table(width, height):
    text = "BeginnerLuft gGmbH - Bandelstr. 1 - 10559 Berlin - www.beginnerluft.de"

    width_list = [
        0.1 * width,
        0.8 * width,
        0.1 * width,
    ]

    res = Table([
        ["", text, ""]
        ],
        rowHeights=height,
        colWidths=width_list
    )

    color = "#FFFF00"
    # color = colors.darkgrey
    res.setStyle([
        # ("GRID", (0, 0), (-1, -1), 1, "red"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        # ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TEXTCOLOR", (0, 0), (-1, -1), "black"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # horizontal
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    ])
    return res
||||||| 674af40
=======


from reportlab.platypus import Table
from reportlab.lib import colors


def gen_footer_table(width, height):
    text = "BeginnerLuft gGmbH - Bandelstr. 1 - 10559 Berlin - www.beginnerluft.de"

    width_list = [
        0.1 * width,
        0.8 * width,
        0.1 * width,
    ]

    res = Table([
        ["", text, ""]
        ],
        rowHeights=height,
        colWidths=width_list
    )

    color = "#FFFF00"
    # color = colors.darkgrey
    res.setStyle([
        # ("GRID", (0, 0), (-1, -1), 1, "red"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        # ("BACKGROUND", (0, 0), (-1, -1), color),
        ("TEXTCOLOR", (0, 0), (-1, -1), "black"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # horizontal
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

    ])
    return res
>>>>>>> a9e9800e95ddb04d17fb9f16cf9433cec7ae1a39
