from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

HEADER = ['#', 'Ингредиент', 'Кол-во', 'Ед.изм.']


def get_invoice(ingredients, buffer):
    data = [HEADER]
    for row, ingredient in enumerate(ingredients):
        data.append([
            row + 1,
            ingredient['ingredient__name'],
            ingredient['total_amount'],
            ingredient['ingredient__measurement_unit']
        ])

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    table = Table(
        data,
        [1 * cm, 12 * cm, 2 * cm, 4 * cm],
        len(data) * [1 * cm])
    table.setStyle(
        TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.02 * cm, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.035 * cm, colors.black),
                    ('FONT', (0, 0), (-1, -1), 'DejaVuSerif', 14),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
    elements.append(table)
    doc.build(elements)
