from reportlab.platypus import Table, Image


def gen_header_table(width, height):

    width_list = [
        0.1 * width,
        0.55 * width,
        0.45 * width,
    ]

    img_path = "resources/beginnerluft.png"
    img_width = width_list[1] * 0.3
    img_height = height * 0.5
    img = Image(filename=img_path, width=img_width, height=img_height, kind="proportional")

    res = Table([
        ["", img, ""],
    ],
        colWidths=width_list,
        rowHeights=height
    )

    res.setStyle([
        # ("GRID", (0, 0), (-1, -1), 1, "red"),
        # ("LEFTPADDING", (0, 0), (-1, -1), 0),
        # ("BACKGROUND", (0, 0), (-1, -1), color),
        # ("TEXTCOLOR", (0, 0), (-1, -1), "white"),
        ("ALIGN", (0, 0), (1, 1), "LEFT"),  # horizontal
        ("VALIGN", (0, 0), (1, 1), "MIDDLE"),
        ("LEFTPADDING", (-1, 0), (-1, 0), -width_list[1] + 98),  # unit is points
        ("FONTSIZE", (2,0), (2,0), 16),
        ("BOTTOMPADDING", (2, 0), (2, -1), 50),
        # ("LINEBELOW", (0,0), (-1,0), 1, "grey"),
    ])

    return res