from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph, Table, ListItem, ListFlowable, Spacer

from app.blueprints.report import BaseReport
from app.blueprints.report import getReportStyleSheet, HorizontalTableStyle


class QualityControlReport(BaseReport):
    def __init__(self, id, pagesize=letter, topMargin=1*inch, leftMargin=1*inch, rightMargin=1*inch, bottomMargin=1*inch):
       super().__init__(id, pagesize, topMargin, leftMargin, rightMargin, bottomMargin)
       self.stylesheet = getReportStyleSheet()

    def make_title(self, title):
        # add title in uppercase with underline
        new_title = f"<u>{title}</u>"
        paragraphe = Paragraph(new_title, self.stylesheet["title"])
        self.flowables.append(paragraphe)
        # add created time
        today = date.today().strftime("%m/%d/%Y")
        date_string = f"<br/>Created Date: {today}"
        paragraphe = Paragraph(date_string, self.stylesheet["date"])
        self.flowables.append(paragraphe)

    def make_horizontal_table(self, heading, data, colWidth):
        # add table heading
        paragraph = Paragraph(heading, self.stylesheet["th1"])
        self.flowables.append(paragraph)

        # transfer each cell into Paragraph which can wrap
        for row in range(len(data)):
            for col in range(len(data[row])):
                if isinstance(data[row][col], str):
                    p = Paragraph(data[row][col], self.stylesheet["Normal"])
                    data[row][col] = p
        
        table = Table(data, colWidths=colWidth)
        table.setStyle(HorizontalTableStyle)
        self.flowables.append(table)

    def make_section_header(self, heading):
        # add section header
        spacer = Spacer(1, 12)
        self.flowables.append(spacer)
        paragraph = Paragraph(heading, self.stylesheet["sh"])
        self.flowables.append(paragraph)

    def make_subsecion_header(self, heading):
        # add subsection header
        paragraph = Paragraph(f"-  {heading}", self.stylesheet["ssh"])
        self.flowables.append(paragraph)

    def make_subsection_bullet_list(self, list_data):
        # add items
        # list_items = []
        for item in list_data:
            # list_items.append(Spacer(width=20, height=1))
            self.flowables.append(Paragraph(f"\u2022  {item}", self.stylesheet['ssb']))
        
        # list_items = [Paragraph(item, self.stylesheet['Normal'])) for item in list_data]
        # list_items = [ListItem(Paragraph(f"\u2022{item}", self.stylesheet['ssb'])) for item in list_data]
        # list_flowable = ListFlowable(list_items, bulletType=None)
        # self.flowables.append(list_flowable)

    def make_subsection_bullet_hyperlink(self, link, text):
        new_link = f'<a href="{link}">{text}</a>'
        self.flowables.append(Paragraph(f"\u2022 {new_link}", self.stylesheet['HyperLink']))

    def make_bullet_list(self, heading, list_data):
        # # add list head
        # paragraph = Paragraph(heading, self.stylesheet["th1"])
        # self.flowables.append(paragraph)

        # add items
        list_items = [ListItem(Paragraph(item, self.stylesheet['Normal'])) for item in list_data]
        list_flowable = ListFlowable(list_items, bulletType='bullet')
        self.flowables.append(list_flowable)

    def make_hyperlink(self, type, link):
        if type == "bullet":
            list_itmes = [ListItem(Paragraph(link, self.stylesheet['HyperLink']))]
            list_flowables = ListFlowable(list_itmes, bulletType='bullet')
            self.flowables.append(list_flowables)




