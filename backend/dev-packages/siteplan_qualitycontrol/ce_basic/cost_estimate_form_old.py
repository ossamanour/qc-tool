import os
import pandas as pd
from pandas import DataFrame
import re

from siteplan_qualitycontrol.ce_basic import price_sheet_template_load


class CostEstimateForm():
    def __init__(self, form_path=None, template_name="SEG.csv"):
        self.form_path = form_path
        if os.path.exists(self.form_path):
            self.df = pd.read_csv(form_path)
        else:
            # create a new file from the template
            self.df = price_sheet_template_load(template_name)
            self.save()
    
    def save(self):
        self.df.to_csv(self.form_path)

    def quantity_update(
            self, 
            description: str = None, 
            quantity: float = 0, 
            input_unit: str = None):
        # get the row for the need to be update item
        idx = self.df[self.df["Description"] == description].index.tolist()[0]
        series = self.df.iloc[idx]

        # get unit and unit price
        unit = series["Unit"]
        price = series["Price per Unit"]
        price = eval((re.sub(r'[^0-9.]', '', price).strip()))

        # if unit consist, direct add
        if unit == input_unit:
            self.df.at[idx, "Quantity"] = quantity
            self.save()
            return f"{description} updated"
        
        # other cases
        if unit == "SY" and input_unit == "SF":
            # SY = SF / 9
            quantity = quantity / 9
            self.df.at[idx, "Quantity"] = quantity
            self.save()
            return f"{description} updated"
        
        if unit == "LY"  and input_unit == "LF":
            # LY = LF / 3
            quantity = quantity / 3
            self.df.at[idx, "Quantity"] = quantity
            self.save()
            return f"{description} updated"
        
        return "unit not working"