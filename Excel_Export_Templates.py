import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from copy import deepcopy, copy
from tkinter.filedialog import asksaveasfilename
from tkinter import Tk
from datetime import *
from config import config
import psycopg2
import re


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

        root = Tk()
        root.withdraw()  # Hiding main window Tkinter

    def save_excel(self):
        # Dialog window to select folder and file name; if path is selected, excel file is saved
        output_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar archivo de Excel")
        if output_path:
            self.wb.save(output_path)


class offer_flow():
    def __init__(self,numoffer,username,rev,project,delivery_term,delivery_time,validity,pay_term,testinspection,revchanges,notes):
        date_offer = date.today().strftime("%d/%m/%Y")
        offername_commercial = numoffer + '-' + 'Commercial.Rev' + rev
        offername_technical = numoffer + '-' + 'Technical.Rev' + rev

        query_commercial = ("""
                    SELECT name, surname, email
                    FROM users_data.registration
                    WHERE username = %s
                    """)
        query_dataoffer = ("""
                        SELECT client, num_ref_offer
                        FROM offers
                        WHERE UPPER (num_offer) LIKE UPPER('%%'||%s||'%%')
                        """)
        query_tagsdata = ("""
                        SELECT *
                        FROM tags_data.tags_flow
                        WHERE UPPER ("num_offer") LIKE UPPER('%%'||%s||'%%')
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur=conn.cursor()

            cur.execute(query_dataoffer,(numoffer,))
            results_offer = cur.fetchall()
            client = results_offer[0][0]
            num_ref = results_offer[0][1]

            cur.execute(query_commercial,(username,))
            results_commercial = cur.fetchall()
            responsible = results_commercial[0][0] + ' ' + results_commercial[0][1]
            email = results_commercial[0][2]

            cur.execute(query_tagsdata,(numoffer,))
            data_tags = cur.fetchall()

            columns=[]
            for elt in cur.description:
                columns.append(elt[0])

            value_type_dict = {'F+P':1, 'F':1, 'P':1, 'M.RUN':1, 'C. RING':1, 'F+C.RING':1, 'RO':1, 'MULTISTAGE RO':1,
                                'WEDGE':2,
                                'PITOT':3,
                                'VFM':4, 'VFW':4, 'VWM':4, 'VWW':4,
                                'NOZZLE BF':5, 'NOZZLE BW':5, 'NOZZLE F':5, 'PTC-6':5}

            df = pd.DataFrame(data=data_tags,columns=columns)
            df['value_type'] = df['item_type'].map(value_type_dict)
            df = df.sort_values(by=['tag', 'value_type'])
            df = df.iloc[:,1:30]
            df['amount'] = df['amount'].apply(self.euros_to_float)

            num_column_amount = df.columns.get_loc("amount") + 1
            number_items = df.shape[0]
            documentation = number_items * 30

        # Loading Excel Template
            self.wb_commercial = load_workbook(r"\\nas01\DATOS\Comunes\EIPSA-ERP\Plantillas Exportación\PLANTILLA OFERTA CAUDAL.xlsx")    

        # Editing sheet COVER
            sheet_name = "COVER"
            ws = self.wb_commercial[sheet_name]
            ws['E4'] = client
            ws['E6'] = offername_commercial
            ws['E8'] = num_ref
            ws['E10'] = project
            ws['E12'] = date_offer
            ws['E14'] = delivery_term
            ws['E16'] = validity
            ws['C43'] = responsible
            ws['C45'] = email

        # Editing sheet EQUIPMENT DATA
            sheet_name = "PRUEBAS DATA"
            ws = self.wb_commercial[sheet_name]
            ws['J3'] = date_offer
            ws['J4'] = num_ref
            ws['J5'] = offername_commercial
            if revchanges != '':
                ws['L5'] = rev + ' ' + revchanges
                ws['L5'].font = Font(name='Calibri', size=14, bold=True)
                ws['L5'].fill = PatternFill("solid", fgColor="FFFF00")

            last_row = 9

            for col_num, col_name in enumerate(df.columns, start=1):
                ws.cell(row=last_row, column=col_num).value = col_name

            for index, row in df.iterrows():    # Data in desired row
                for col_num, value in enumerate(row, start=1):
                    cell = ws.cell(row=last_row + 1 + index, column=col_num)
                    cell.value = value
                    if col_num == num_column_amount:
                        cell._style = ws['X1']._style
                    else:
                        cell._style = ws['S1']._style

            last_row = ws.max_row
            ws[f'A{last_row+3}'] = "Offer Validity: " + validity + " days"
            ws.cell(row=last_row+3, column=num_column_amount - 1).value = "QTY. TOTAL"
            ws.cell(row=last_row+3, column=num_column_amount).value = number_items
            ws[f'A{last_row+4}'] = "Delivery Time: " + delivery_time + " weeks since drawing / calculation approval (August and last two December weeks excluded)"
            ws.cell(row=last_row+5, column=num_column_amount - 1).value = "TOTAL AMOUNT OF MATERIAL"
            ws.cell(row=last_row+5, column=num_column_amount).value = f'=SUM({get_column_letter(num_column_amount)}{10}:{get_column_letter(num_column_amount)}{last_row})'
            ws.cell(row=last_row+7, column=num_column_amount - 1).value = "PACKING AND TRANSPORT (FCA 2020)"
            ws.cell(row=last_row+7, column=num_column_amount).value = f'=MROUND({get_column_letter(num_column_amount)}{last_row+5}*0.03,10)'
            ws.cell(row=last_row+8, column=num_column_amount - 1).value = "TESTS & INSPECTION"
            ws.cell(row=last_row+8, column=num_column_amount).value = float(testinspection)
            ws.cell(row=last_row+9, column=num_column_amount - 1).value = "DOCUMENTATION"
            ws.cell(row=last_row+9, column=num_column_amount).value = documentation
            ws.cell(row=last_row+11, column=num_column_amount - 1).value = "TOTAL AMOUNT OF BID"
            ws.cell(row=last_row+11, column=num_column_amount).value = f'=SUM({get_column_letter(num_column_amount)}{last_row+5}:{get_column_letter(num_column_amount)}{last_row+9})'
            ws[f'A{last_row+3}']._style = ws['R1']._style
            ws.cell(row=last_row+3, column=num_column_amount - 1)._style = ws['R1']._style
            ws.cell(row=last_row+3, column=num_column_amount).font = Font(name='Calibri', size=14)
            ws[f'A{last_row+4}']._style = ws['R1']._style
            ws.cell(row=last_row+5, column=num_column_amount - 1)._style = ws['R1']._style
            ws.cell(row=last_row+5, column=num_column_amount)._style = ws['T1']._style
            ws.cell(row=last_row+7, column=num_column_amount - 1).font = Font(name='Calibri', size=14)
            ws.cell(row=last_row+7, column=num_column_amount)._style = ws['T1']._style
            ws.cell(row=last_row+8, column=num_column_amount - 1).font = Font(name='Calibri', size=14)
            ws.cell(row=last_row+8, column=num_column_amount)._style = ws['T1']._style
            ws.cell(row=last_row+9, column=num_column_amount - 2)._style = ws['U1']._style
            ws.cell(row=last_row+9, column=num_column_amount - 1)._style = ws['U1']._style
            ws.cell(row=last_row+9, column=num_column_amount)._style = ws['V1']._style
            ws.cell(row=last_row+11, column=num_column_amount - 1)._style = ws['R1']._style
            ws.cell(row=last_row+11, column=num_column_amount)._style = ws['W1']._style

            if notes != '':
                notes = notes.split("\n")
                line = last_row+5
                for note in notes:
                    ws[f'A{line}'] = note
                    ws[f'A{line}']._style = ws['R1']._style
                    line += 1

        # Editing sheet NOTES
            sheet_name = "NOTES"    # Selecting  sheet
            ws = self.wb_commercial[sheet_name]
            ws['B11'] = "Delivery time " + delivery_time + " weeks since drawing / calculation approval (August and last two December weeks excluded)."
            ws['B12'] = "Plazo de entrega " + delivery_time + " semanas desde aprobación de planos y cálculos (Agosto y las dos últimas semanas de diciembre excluidos)."
            if pay_term == '100':
                ws['B53'] = "client-a"
                ws['B54'] = "variable-a"
            if pay_term == '90_10':
                ws['B53'] = ("PAYMENT TERMS:\n"
                            "a) 90 % of the total amount of PO upon delivery of material according to Incoterms 2020, FCA (our facilities, Spain) and 10% at take over certificate. \n"
                            "Bank Transfer: 60 days since invoice issue date.")
                ws['B54'] = ("TERMINOS DE PAGO:\n"
                            "a) Pago del 90% del Valor total de la orden de compra a la entrega del material según Incoterm 2020, FCA (nuestras instalaciones, España) y el 10% restante con la certificación final.\n"
                            "Transferencia Bancaria: 60 días desde emision de factura.")
            if pay_term == '50_50':
                ws['B53'] = "client"
                ws['B54'] = "variable"
            if pay_term == 'Others':
                ws['B53'] = "PAYMENT TERMS TO BE DEFINED"
                ws['B53'].font = Font(name='Calibri', size=11, bold=True, color="FF0000")
                ws['B54'] = "TERMINOS DE PAGO POR DEFINIR"
                ws['B54'].font = Font(name='Calibri', size=11, bold=True, italic=True, color="FF0000")
            ws['A62'] = ("If you require further information related with this offer, please do not hesitate to contact:\n"
                        + responsible + "\n"
                        + email + "\n"
                        "Telf.: (+34) 916.582.118")

            std=self.wb_commercial.get_sheet_by_name('Pitot')
            self.wb_commercial.remove_sheet(std)

            path = self.save_excel_commercial()

        # Creating the technical offer using the commercial one as template
            self.wb_technical = load_workbook(path)

            sheet_name = "COVER"
            ws = self.wb_technical[sheet_name]
            ws['E6'] = offername_technical

            sheet_name = "PRUEBAS DATA"
            ws = self.wb_technical[sheet_name]
            ws['J5'] = offername_technical

            ws.cell(row=last_row+3, column=num_column_amount - 1).value = ""
            ws.cell(row=last_row+5, column=num_column_amount - 1).value = ""
            ws.cell(row=last_row+7, column=num_column_amount - 1).value = ""
            ws.cell(row=last_row+8, column=num_column_amount - 1).value = ""
            ws.cell(row=last_row+9, column=num_column_amount - 1).value = ""
            ws.cell(row=last_row+11, column=num_column_amount - 1).value = ""
            ws.cell(row=last_row+9, column=num_column_amount - 2)._style = ws['AA1']._style
            ws.cell(row=last_row+9, column=num_column_amount - 1)._style = ws['AA1']._style

            self.wb_technical["PRUEBAS DATA"].delete_cols(num_column_amount,1)

            std=self.wb_technical.get_sheet_by_name('1.3')
            self.wb_technical.remove_sheet(std)

            self.save_excel_technical()

            root = Tk()
            root.withdraw()  # Hiding main window Tkinter

        # close communication with the PostgreSQL database server
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def euros_to_float(self, value):
        value=value.replace(".","")
        value=value.replace(",",".")
        value=value[:value.find(" €")]
        return float(value)

    def save_excel_commercial(self):
        # Dialog window to select folder and file name; if path is selected, excel file is saved
        output_path_commercial = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar Oferta comercial")
        if output_path_commercial:
            self.wb_commercial.save(output_path_commercial)
            return output_path_commercial

    def save_excel_technical(self):
        output_path_technical = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar Oferta técnica")
        if output_path_technical:
            self.wb_technical.save(output_path_technical)