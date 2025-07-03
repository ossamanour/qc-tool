"""
Class for cost estimate price sheet form.
"""
import os
import pandas as pd
import re

from siteplan_qualitycontrol.ce_basic import price_sheet_template_load


class CostEstimateForm():
    def __init__(self, form_path=None, template_name="SEG.xlsx"):
        self.form_path = form_path
        if os.path.exists(self.form_path):
            self.form = pd.read_excel(form_path, sheet_name=None)
            self.onsite_df = self.form["onsite"]
            self.offsite_df = self.form["offsite"]
        else:
            # create a new file from the template
            self.form = price_sheet_template_load(template_name)
            self.onsite_df = self.form["onsite"]
            self.offsite_df = self.form["offsite"]
            self.save()

    def save(self):
        with pd.ExcelWriter(self.form_path, engine="openpyxl") as writer:
            self.onsite_df.to_excel(writer, sheet_name="onsite", index=False)
            self.offsite_df.to_excel(writer, sheet_name="offsite", index=False)
    
    def update_save(self, sheet_name: str = None):
        if sheet_name == "onsite":
            self.onsite_df = self.df
        elif sheet_name == "offsite":
            self.offsite_df = self.df
        self.save()

    def quantity_update(
            self, 
            sheet_name: str = None, 
            description: str = None, 
            quantity: float = 0., 
            input_unit: str = None):
        # based on the sheet name, decide which sheet to be modified
        if sheet_name == "onsite":
            self.df = self.onsite_df
        elif sheet_name == "offsite":
            self.df = self.offsite_df
        
        # get the row for the need-to-be-updated item
        idx = self.df[self.df["Description"] == description].index.tolist()[0]
        series = self.df.iloc[idx]

        # get unit and unit price
        unit = series["Unit"]
        price = series["Price per Unit"]
        # when using excel, unlike csv, the $ is ignored automatically
        # price = eval((re.sub(r'[^0-9.]', '', price).strip()))

        # if unit consist, direct add
        if unit == input_unit:
            self.df.at[idx, "Quantity"] = quantity
            self.update_save(sheet_name)
            return f"{sheet_name}-{description} updated"
        
        # other cases
        if unit == "SY" and input_unit == "SF":
            # SY = SF / 9
            quantity = quantity / 9
            self.df.at[idx, "Quantity"] = quantity
            self.update_save(sheet_name)
            return f"{sheet_name}-{description} updated"
        
        if unit == "LY"  and input_unit == "LF":
            # LY = LF / 3
            quantity = quantity / 3
            self.df.at[idx, "Quantity"] = quantity
            self.update_save(sheet_name)
            return f"{sheet_name}-{description} updated"
        
        return "unit not working"
            

        