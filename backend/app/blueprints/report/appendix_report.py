from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph, Image, PageBreak, Spacer  

from app.blueprints.report import BaseReport
from app.blueprints.report import getReportStyleSheet

class AppendixReport(BaseReport):
    def __init__(self, id, pagesize=letter, topMargin=1*inch, leftMargin=1*inch, rightMargin=1*inch, bottomMargin=1*inch):
       super().__init__(id, pagesize, topMargin, leftMargin, rightMargin, bottomMargin)
       self.stylesheet = getReportStyleSheet()

    def make_image(self, title, image_path, width, height):
        # add title
        paragraph = Paragraph(title, self.stylesheet["ah1"])
        self.flowables.append(paragraph)
        # add image
        image = Image(image_path, width=width, height=height)
        self.flowables.append(image)

    def make_newpage(self):
        self.flowables.append(PageBreak())

    def make_coverpage(self, title):
        # add title
        spacer = Spacer(1, 8*inch)
        self.flowables.append(spacer)
        paragraph = Paragraph(title, self.stylesheet["a_title"])
        self.flowables.append(paragraph)
        

