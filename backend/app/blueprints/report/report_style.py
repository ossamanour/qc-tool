from reportlab.lib.colors import white, black, gray, blue
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.fonts import tt2ps
from reportlab.rl_config import canvas_basefontname as _baseFontName
_baseFontNameB = tt2ps(_baseFontName,1,0)
_baseFontNameI = tt2ps(_baseFontName,0,1)
_baseFontNameBI = tt2ps(_baseFontName,1,1)

from reportlab.lib.styles import PropertySet
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import TableStyle


# self defined style sheet object based on StyleSheet1
def getReportStyleSheet():
    stylesheet = StyleSheet1()

    # base
    stylesheet.add(ParagraphStyle(name="Normal", 
                                  fontName=_baseFontName, 
                                  fontSize=10, 
                                  leading=12))
    
    # title
    stylesheet.add(ParagraphStyle(name="Title", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB, 
                                  fontSize=20, 
                                  leading=16, 
                                  alignment=TA_CENTER, 
                                  spaceAfter=6, 
                                  textTransform="uppercase"), alias="title")

    # date
    stylesheet.add(ParagraphStyle(name="Date", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB,
                                  leading=12,
                                  alignment=TA_CENTER), alias="date")

    # section heading
    stylesheet.add(ParagraphStyle(name="SectionHeading", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB, 
                                  fontSize=12, 
                                  leading=20, 
                                  spaceBefore=6,
                                  spaceAfter=6, 
                                  textTransform="uppercase"), alias="sh")
    
    # subsection heading
    stylesheet.add(ParagraphStyle(name="SubSectionHeading", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB, 
                                  fontSize=10, 
                                  leading=20,
                                  leftIndent=10,  
                                  spaceBefore=6,
                                #   spaceAfter=6, 
                                  textTransform="capitalize"), alias="ssh")

    # subsection bullet item
    stylesheet.add(ParagraphStyle(name="SubsetionBulletItem1", 
                                  parent=stylesheet["Normal"], 
                                  leftIndent=20,), alias="ssb")

    # TableHeading1
    stylesheet.add(ParagraphStyle(name="TableHeading1", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB, 
                                  fontSize=12, 
                                  leading=20, 
                                  spaceBefore=6,
                                  spaceAfter=6, 
                                  textTransform="uppercase"), alias="th1")
    
    # bullet item
    stylesheet.add(ParagraphStyle(name="BulletItem1", 
                                  parent=stylesheet["Normal"], 
                                  leftIndent=20,
                                  bulletIndent=20, 
                                  bulletType="arrowhead"), alias="bi1")
    
    # hyperlink
    stylesheet.add(ParagraphStyle(name="HyperLink", 
                                  parent=stylesheet["SubsetionBulletItem1"], 
                                  bulletIndent=20, 
                                  bulletType="arrowhead", 
                                  linkUnderline=True, 
                                  textColor=blue), alias="hl")
    
    # appendix title
    stylesheet.add(ParagraphStyle(name="AppenTitle", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB, 
                                  fontSize=100, 
                                  leading=16, 
                                  alignment=TA_CENTER, 
                                  spaceAfter=6, 
                                  textTransform="uppercase"), alias="a_title")
    
    # appendix heading
    stylesheet.add(ParagraphStyle(name="AppendixHeading1", 
                                  parent=stylesheet["Normal"], 
                                  fontName=_baseFontNameB, 
                                  fontSize=20, 
                                  leading=20, 
                                  spaceBefore=6,
                                  spaceAfter=6, 
                                  textTransform="uppercase"), alias="ah1")

    return stylesheet

HorizontalTableStyle = TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Oblique'),
    ('BACKGROUND', (1,0), (-1,-1), colors.white),
    ('FONTNAME', (1,0), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('FONTSIZE', (0,0), (-1,-1), 12),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
])

CostTableStyle = TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Oblique'),
    ('BACKGROUND', (0,1), (-1,-1), colors.white),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('FONTSIZE', (0,0), (-1,-1), 12),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
])
# def getTableStyle():
#     tablestyle = TableStyle([
#         ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
#         ('FONTNAME', (0,0), (0,-1), 'Helvetica-Oblique'),
#         ('BACKGROUND', (1,0), (-1,-1), colors.white),
#         ('FONTNAME', (1,0), (-1,-1), 'Helvetica'),
#         ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
#         ('ALIGN', (0,0), (-1,-1), 'LEFT'),
#         ('FONTSIZE', (0,0), (-1,-1), 12),
#         ('TOPPADDING', (0,0), (-1,-1), 2),
#         ('BOTTOMPADDING', (0,0), (-1,-1), 2),
#         ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#     ])

#     return tablestyle

