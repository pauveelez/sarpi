from config import USER_SARPI, PSW_SARPI, OWNER_MAIL, FROM_MAIL

# Correo
import smtplib

# Configuracion Celery
from celery import Celery

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

# Definicion de las tareas programadas de SARpi

from sarpi import sarpi, db
from datetime import datetime, date
from sarpi.models import Pet, PetWeight, Schedule, Owner

# Ver los estados de los horarios, los retorna en una lista
def state_schedules(state):
    list_schedules = Schedule.query.filter_by(state = state).order_by(Schedule.date_start)
    list_done = []
    for schedule in list_schedules.all():
        list_done.append(schedule)

    return list_done

# Cambia el estado de un schedule especifico pasando como parametro el id del schedule y el state al que se desea cambiar
def change_state(scheduleId, state):
    schedule = Schedule.query.get(scheduleId)
    schedule.state = state
    db.session.commit()

# Para enviar correo
def noticeEMail(description, dateS, timeS):
    usr= USER_SARPI
    psw= PSW_SARPI
    fromaddr= FROM_MAIL
    toaddr= OWNER_MAIL

    # Initialize SMTP server
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    # Send email
    senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
    subject="You have a fail schedule in SARpi"
    m="Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (senddate, fromaddr, toaddr, subject)
    msg='''

    Hola algo paso con SARpi y el schedule: '''+description+ ''' del dia '''+dateS+ ''' a las '''+timeS+ ''' no fue realizado '''

    server.sendmail(fromaddr, toaddr, m+msg)
    server.quit()

# [Tarea] Busca los horarios en estado to_do y el dia y la hora del momento para ver si tiene que abrir el alimentador; luego de eso pasa el state = to_do a state = done para indicar que ya cumplio el horario programado
@celery.task
def schedule_feed():
    schedules_to_do = state_schedules('to_do')
    dateToday = date.today()
    for schedule in schedules_to_do:

        timeNow = datetime.now().time().strftime('%H:%M:00')

        if schedule.date_start == dateToday:
            timeSchedule = schedule.time_start.strftime('%H:%M:00')
            if timeSchedule == timeNow:
                print 'Codigo SARpi GPIO'
                # Se actualiza el state de to_do a done ya que se cumplio con el horario
                change_state(schedule.id, 'done')

# [Tarea] Busca los horarios que estan en to_do y verifica que no se halla pasado la hora de alimentar a la mascota y/o el dia, si esto es asi cambia el estado a fail ya que no se cumplio con el horario programado y le manda una notificacion al usuario
@celery.task
def schedule_fail():
    schedules_to_do = state_schedules('to_do')
    dateToday = date.today()
    for schedule in schedules_to_do:

        dateSchedule = schedule.date_start
        timeNow = datetime.now().time()
        timeSchedule = schedule.time_start

        if dateSchedule == dateToday:
            if timeSchedule < timeNow:
                # Se actualiza el state de to_do a fail ya que paso la hora programada y el horario sigue en to_do, es decir no se alimento a la mascota
                change_state(schedule.id, 'fail')
                print 'mandar notificacion'
                description = schedule.description
                dateS = dateSchedule.strftime("%d-%m-%y")
                timeS = timeSchedule.strftime('%H:%M:00')
                noticeEMail(description, dateS, timeS)

        elif dateSchedule < dateToday:
            print 'mandar notificacion'
            # Se actualiza el state de to_do a fail ya que paso el dia y el horario sigue en to_do, es decir no se alimento a la mascota
            change_state(schedule.id, 'fail')
            description = schedule.description
            dateS = dateSchedule.strftime("%d-%m-%y")
            timeS = timeSchedule.strftime('%H:%M:00')
            noticeEMail(description, dateS, timeS)