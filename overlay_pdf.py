import os
from fpdf import FPDF
import io
import pandas as pd

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

# Function to create PDF with specific note in a position
def new_content_notes(technical_note):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        technical_note (str): The content to be added to the PDF.

    Returns:
        io.BytesIO: A byte stream containing the generated PDF.
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('COURIERTXT', '', os.path.abspath(os.path.join(basedir, "Resources/Iconos/COURIERTXT.ttf")))
    pdf.set_font("courier", "", 10)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.set_xy(20,230)
    pdf.set_font("courier", "B", 10)
    pdf.cell(150, 5, "NOTES:")
    pdf.set_xy(20,235)
    pdf.set_font("courier", "", 10)
    pdf.multi_cell(150, 5, str(technical_note)) #x_position, y_position, technical_note)

    return io.BytesIO(pdf.output())


# Function to create PDF with specific text in a position
def new_content_tags(value, type_eq):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        value (str): The content to be added to the PDF.
        type_eq (str): The type of equipment, determining the positioning in the PDF.

    Returns:
        io.BytesIO: A byte stream containing the generated PDF.
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)

    excel_file = r"\\nas01\DATOS\Comunes\EIPSA-ERP\Plantillas Importación\Importar Tags Cálculos.xlsx"
    df_data = pd.read_excel(excel_file, sheet_name='Posiciones')
    df_data = df_data.set_index('type')

    x_position = df_data['x(mm)'][type_eq]
    y_position = df_data['y(mm)'][type_eq]

    if type_eq == 'MUL':
        pdf.add_page()
        pdf.set_xy(x_position, y_position)
        with pdf.rotation(90):
            pdf.cell(10, 10, value)

    else:
        pdf.add_page()
        pdf.text(x_position, y_position, value)

    return io.BytesIO(pdf.output())


def drawing_number(drawing, counter):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_xy(163, 262)

    pdf.cell(37, 7, f"{str(drawing.split('.')[0])}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())


def flange_dwg_flangedTW(num_order, material, count):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1.5)
    pdf.set_draw_color(92, 197, 229)
    pdf.rect(20, 8, 185, 282, style='D')

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())


def bar_dwg_flangedTW(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1.5)
    pdf.set_draw_color(92, 197, 229)
    pdf.rect(20, 8, 185, 282, style='D')

    total_count = 0

    pdf.set_xy(27, 20)

    for bore, std_len, cnt in item_data:
        pdf.cell(15, 5, str(cnt), align='C')
        pdf.cell(15, 5, str(bore), align='C')
        pdf.cell(15, 5, str(int(std_len) + 10), align='C')
        pdf.ln()
        total_count += cnt

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(total_count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())