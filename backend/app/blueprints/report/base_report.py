import os
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph
from PyPDF2 import PdfReader, PdfWriter


class BaseReport():
    def __init__(self, id, pagesize=letter, topMargin=1*inch, leftMargin=1*inch, rightMargin=1*inch, bottomMargin=1*inch):
        self.id = id
        
        # create buffer
        self.buffer = BytesIO()

        # create SimpleDocTmeplate for report
        self.doc = SimpleDocTemplate(
            self.buffer, 
            pagesize=pagesize, 
            topMargin=topMargin, 
            leftMargin=leftMargin, 
            rightMargin=rightMargin, 
            bottomMargin=bottomMargin)
        self.flowables = []

    def build(self):
        # build pdf file
        self.doc.build(self.flowables)

    def save(self, filepath):
        with open(filepath, "wb") as pdf_file:
            pdf_file.write(self.buffer.getvalue())

    def build_and_save(self, filepath):
        self.build()
        self.save(filepath)

    

class MultiSizeReport():
    def __init__(self, config_dict):
        """
        config_dict structure:
            [{id: xxx, 
              pagesize: xxx, 
              topMargin: xxx, 
              leftMargin: xxx, 
              bottomMargin: xxx}}, 
             {...},
            ]
        """
        # create a buffer for the whole
        self.buffer = BytesIO()

        # create base list
        self.report_list = []

        for item in config_dict:
            self.report_list.append(BaseReport(
                id=item.id, 
                pagesize=item.pagesize, 
                topMargin=item.topMargin, 
                leftMargin=item.leftMargin, 
                rightMargin=item.rightMargin, 
                bottomMargin=item.bottomMargin))
    
    def build(self):
        # combine all pdf together
        pdf_writer = PdfWriter()
        for report in self.report_list:
            report.build()
            pdf = PdfReader(report.buffer)
            for page in pdf.pages:
                pdf_writer.add_page(page)
        # write the whole to the buffer
        pdf_writer.write(self.buffer)

    def save(self, filepath):
        with open(filepath, "wb") as pdf_file:
            pdf_file.writte(self.buffer.getvalue())

    def get(self, id):
        for item in self.report_list:
            if item["id"] == id:
                return item
        
        return None




