import pandas as pd
from openpyxl import load_workbook
from copy import deepcopy
from tkinter.filedialog import asksaveasfilename
from tkinter import Tk
from datetime import *


class material_order():
    def __init__(self,df,num_order,client,variable,num_ot):
        self.wb = load_workbook(r"\\nas01\DATOS\Comunes\EIPSA-ERP\Plantillas Exportación\Pedido Materia Prima.xlsx")    # Loading Excel Template
        sheet_name = "Hoja1"    # Selecting template sheet
        ws = self.wb[sheet_name]
        start_row = 12    # Obtaining last row used
        row_11_style = {}
        for col_num in range(1, 15):
            cell_11 = ws.cell(row=12, column=col_num)
            row_11_style[col_num] = deepcopy(cell_11._style)

        for index, row in df.iterrows():
            for col_num, value in enumerate(row, start=4):
                cell = ws.cell(row=start_row + index, column=col_num)
                cell.value = value
                for num in range(1, 15):
                    cell = ws.cell(row=start_row + index, column=num)
                    cell._style = deepcopy(row_11_style[num])

        # Adding text in cell L4, C5, C6, H1 and H9
        ws['L4'] = num_order
        ws['C5'] = client
        ws['C6'] = variable
        ws['H1'] = int(num_ot)
        ws['H9'] = date.today().strftime("%d/%m/%Y")

        # cell_P1 = ws['P1']
        # style_P1 = deepcopy(cell_P1._style)
        # ws['H1']._style = style_P1

        root = Tk()
        root.withdraw()  # Hiding main window Tkinter

    def save_excel(self):
        # Dialog window to select folder and file name; if path is selected, excel file is saved
        output_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar archivo de Excel")
        if output_path:
            self.wb.save(output_path)