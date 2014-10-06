import os
from sarpi import sarpi
from config import PDF_FOLDER

from xhtml2pdf import pisa
from StringIO import StringIO

def create_pdf(pdf_data):
    """Creacion de PDF a partir de un template HTML

    :param pdf_data: render template html
    :type pdf_data: str
    """
    resultFile = open(os.path.join(sarpi.config['PDF_FOLDER'], 'file.pdf'), "w+b")
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data), dest=resultFile)
    resultFile.close()
    return pdf

def choises_hours():
    """Es la funcion encargada de llenar el select de las horas"""
    count = 1
    hours = []
    hours.append('0 ')
    for i in range(24):
        for j in range(6):
            h = (str(count), str(i)+':'+str(j)+'0')
            hours.append(h)
            count = count+1
    return hours