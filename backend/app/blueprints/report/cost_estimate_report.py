from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph, Table
import pandas as pd

from app.blueprints.report import BaseReport
from app.blueprints.report import getReportStyleSheet, CostTableStyle


class CostEstimateReport(BaseReport):
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

    def make_cost_table(self, heading, df_data):
        # add table heading
        paragraph = Paragraph(heading, self.stylesheet["th1"])
        self.flowables.append(paragraph)

        # convert pandas dataframe to table data
        data = [df_data.columns.to_list()] + df_data.values.tolist()
        # transfer each cell into Paragraph which can wrap
        for row in range(len(data)):
            for col in range(len(data[row])):
                if isinstance(data[row][col], str):
                    p = Paragraph(data[row][col], self.stylesheet["Normal"])
                    data[row][col] = p
        
        table = Table(data)
        table.setStyle(CostTableStyle)
        self.flowables.append(table)

    def make_subsecion_header(self, heading):
        # add subsection header
        paragraph = Paragraph(f"-  {heading}", self.stylesheet["ssh"])
        self.flowables.append(paragraph)

    def make_subsection_bullet_hyperlink(self, link, text):
        new_link = f'<a href="{link}">{text}</a>'
        self.flowables.append(Paragraph(f"\u2022 {new_link}", self.stylesheet['HyperLink']))

    