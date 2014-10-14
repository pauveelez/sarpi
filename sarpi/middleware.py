import os
from sarpi import sarpi
from config import PDF_FOLDER

from xhtml2pdf import pisa
from StringIO import StringIO

# Descomentar para usar feed_pet
# import RPi.GPIO as GPIO
# from time import sleep

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

def feed_pet(time):
    """Alimentar a la mascota apartir del GPIO del Raspberry Pi, el cual enciende el motor para dejar salir la comida del alimentador
    :param time: el tiempo que el motor esta dando vueltas
    :type time: int
    """
    # GPIO.setmode(GPIO.BOARD)

    Motor1A = 16
    Motor1B = 18
    Motor1E = 22

    # GPIO.setup(Motor1A,GPIO.OUT)
    # GPIO.setup(Motor1B,GPIO.OUT)
    # GPIO.setup(Motor1E,GPIO.OUT)

    print "ON"
    # GPIO.output(Motor1A,GPIO.HIGH)
    # GPIO.output(Motor1B,GPIO.LOW)
    # GPIO.output(Motor1E,GPIO.HIGH)

    timeOn = int(time)
    # sleep(timeOn)

    print "OFF"
    # GPIO.output(Motor1E,GPIO.LOW)

    # GPIO.cleanup()
