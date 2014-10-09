import os
from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required
from sarpi import sarpi, db, lm
from forms import LoginForm, EditFormPet, EditFormOwner, ProgramSchedule, CreateReport
from datetime import datetime, date
from models import Pet, PetWeight, Schedule, Owner
from middleware import create_pdf, choises_hours
# Para subir las imagenes
from werkzeug import secure_filename
from config import UPLOAD_FOLDER, PDF_FOLDER, PDF_DOWNLOAD

#Error Handlers
@sarpi.errorhandler(404)
def page_not_found(e):
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")
    return render_template('404.html',
        title = 'Page not Found',
        time = time,
        pet = pet), 404

@sarpi.errorhandler(500)
def internal_server_error(e):
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")
    return render_template('500.html',
        title = 'Internal Server Error',
        time = time,
        pet = pet), 500

# Login
@lm.user_loader
def load_user(username):
    return Owner.query.get(username)

@sarpi.before_request
def before_request():
    g.owner = current_user

@sarpi.route('/', methods = ['GET', 'POST'])
@sarpi.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = str(form.password.data)
        owner = load_user(username)

        if owner is not None and owner.password == password:
            login_user(owner)
            flash("Logged in successfully. ")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash('El username:'+ username +' no existe')


    return render_template('login.html',
        title = 'Sign In',
        form = form)

@sarpi.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home de SARpi - En adelante debe estar logeado para que se pueda acceder a las diferentes vistas
@sarpi.route('/index')
@login_required
def index():
    today = date.today()
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    schedules_today = Schedule.query.filter(Schedule.date_start == today).filter_by(state = 'to_do').order_by(Schedule.time_start)

    json_results = []
    for schedule in schedules_today:
        date_s = schedule.date_start.strftime("%Y-%m-%d")
        time_s = schedule.time_start.strftime('%H:%M')
        d = {'date_start': date_s,
           'time_start': time_s
            }
        json_results.append(d)

    if json_results:
        return render_template('index.html',
            title = 'Home',
            time = time,
            schedules = json_results,
            pet = pet)
    else:
        return render_template('index.html',
            title = 'Home',
            time = time,
            pet = pet)

#FeedmeNow
@sarpi.route('/ajax_feed', methods = ['GET', 'POST'])
@login_required
def ajax_feed():
    if request.method == 'POST':
        seconds = request.form['seconds']
        print 'Holaaaaaaa'+seconds
        return 'here come de code'

    return 'Hi Code for FeedMeNow - Nothing to do here'


#Datos de la mascota y el usuario
@sarpi.route('/pet/<name>')
@login_required
def pet_data(name):
    pet = Pet.query.filter_by(name = name).first_or_404()
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    weight = PetWeight.query.filter_by(pet_id = pet.id).order_by(PetWeight.date_creation.desc()).first_or_404()

    return render_template('pet.html',
        title = 'Pet Profile',
        time = time,
        pet = pet,
        petWeight = weight)


@sarpi.route('/pet/<name>/edit', methods = ['GET', 'POST'])
@login_required
def pet_data_edit(name):
    pet = Pet.query.filter_by(name = name).first_or_404()
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")
    petWeight = PetWeight.query.filter_by(pet_id = pet.id).order_by(PetWeight.date_creation.desc()).first_or_404()

    form = EditFormPet()

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.type_pet = form.type_pet.data
        if form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(sarpi.config['UPLOAD_FOLDER'], filename))
            pet.url_image = '/static/img/pet/'+filename

        db.session.add(pet)
        db.session.commit()

        weight = float(form.weight.data)
        if weight != petWeight.weight:
            petWeightNew = PetWeight(date_creation = date.today(), weight = weight, pet_id = pet.id)
            db.session.add(petWeightNew)
            db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('pet_data', name = pet.name))

    elif request.method != "POST":
        form.name.data = pet.name
        form.type_pet.data = pet.type_pet
        form.weight.data = petWeight.weight

    return render_template('pet_edit.html',
        title = 'Pet - Edit',
        time = time,
        pet = pet,
        form = form)

@sarpi.route('/owner/edit', methods = ['GET', 'POST'])
@login_required
def owner_edit():
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    form = EditFormOwner()

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        if form.newPassword.data:
            current_user.password = str(form.newPassword.data)

        db.session.add(g.owner)
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('pet_data', name = pet.name))

    elif request.method != "POST":
        form.name.data = g.owner.name
        form.email.data = g.owner.email

    return render_template('owner_edit.html',
        title = 'Owner - Edit',
        pet = pet,
        time = time,
        form = form)

# Manejo de los Horarios
@sarpi.route('/schedule', methods = ['GET', 'POST'])
@login_required
def schedule():
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    schedules_to_do = Schedule.query.filter_by(state = 'to_do').order_by(Schedule.date_start)

    json_results = []
    for schedule in schedules_to_do:
        date_s = schedule.date_start.strftime("%Y-%m-%d")
        time_s = schedule.time_start.strftime('%H:%M:00')
        d = {'description': ''+schedule.description,
           'date_start': date_s,
           'time_start': time_s,
            }
        json_results.append(d)

    return render_template('schedule.html',
        pet = pet,
        time = time,
        schedules = json_results)


@sarpi.route('/schedule/<dateS>', methods = ['GET', 'POST'])
@login_required
def set_schedule(dateS):
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    dateShedule = datetime.strptime(dateS, '%Y-%m-%d').date()
    dateShow = dateShedule.strftime('%d %B %Y')

    form = ProgramSchedule()

    form.hours.choices = [(hour[1], hour[1]) for hour in choises_hours()]

    if form.validate_on_submit():
        hourString = request.form['hours']
        if hourString != '0':
            hour = datetime.strptime(hourString, '%H:%M').time()
            description = form.description.data
            portion = form.portion.data
            shedule = Schedule(description = description, date_start = dateShedule, time_start = hour, portion = portion, pet_id = pet.id, owner_username = g.owner.username)
            db.session.add(shedule)
            selectNumber = request.form['count']
            if selectNumber != '0':
                for i in range(int(selectNumber)):
                    j = i+1
                    hourString = request.form['hours'+str(j)]
                    if hourString:
                        hour = datetime.strptime(hourString, '%H:%M').time()
                        shedule = Schedule(description = description, date_start = dateShedule, time_start = hour, portion = portion, pet_id = pet.id, owner_username = g.owner.username)
                        db.session.add(shedule)
            db.session.commit()
            flash('Your Schedule have been saved.')
            return redirect(url_for('schedule'))
        else:
           flash('Debe seleccionar una hora')

    return render_template('schedule_edit.html',
        title = 'Schedule -'+dateS,
        pet = pet,
        time = time,
        dateShedule = dateShow,
        form = form)

#Cancelar los horarios de una fecha
# Comentado como plan B para eliminar horarios
# @sarpi.route('/schedule_cancel/<dateS>', methods = ['GET', 'POST'])
# @login_required
# def cancel_schedule(dateS):
#     pet = Pet.query.get(1)
#     time = datetime.now().strftime("%d-%m-%Y | %H:%M")

#     dateShedule = datetime.strptime(dateS, '%Y-%m-%d').date()
#     dateShow = dateShedule.strftime('%d %B %Y')

#     schedules_cancel = Schedule.query.filter(Schedule.date_start == dateShedule).filter_by(state = 'to_do').order_by(Schedule.time_start)

#     if request.method == 'POST':
#         Schedule.query.filter(Schedule.date_start == dateShedule).filter_by(state = 'to_do').delete()
#         db.session.commit()
#         flash('The Schedule of '+dateShow+' have been delete')
#         return redirect(url_for('schedule'))

#     return render_template('schedule_cancel.html',
#         title = 'Schedule -'+dateS,
#         pet = pet,
#         time = time,
#         dateShedule = dateShow,
#         schedules = schedules_cancel)

#Cancel Schedule with Ajax
@sarpi.route('/schedule_ajax', methods = ['GET', 'POST'])
@login_required
def schedule_ajax():
    if request.method == 'POST':
        dateShedule = request.form['date']
        dateCancel = datetime.strptime(dateShedule, '%Y-%m-%d').date()
        Schedule.query.filter(Schedule.date_start == dateCancel).filter_by(state = 'to_do').delete()
        db.session.commit()
        print 'The Schedule of '+dateShedule+' have been delete'
        return redirect(url_for('schedule'))

    return 'Hi Code for Cancel Schedule - Nothing to do here'

# Creacion de Reportes - Lista en PDF - Grafica de Pesos
@sarpi.route('/reporte', methods = ['GET', 'POST'])
@login_required
def reports():
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    form = CreateReport()

    if form.validate_on_submit():
        dateS = form.dateStart.data
        dateF = form.dateFinish.data
        type_report = form.type_report.data
        if type_report == '1':
            return redirect(url_for('createpdf', dateS = dateS, dateF = dateF))
        else:
            return redirect(url_for('weight_report', dateS = dateS, dateF = dateF))


    return render_template('reportes.html',
        title = 'Reportes SARpi',
        pet = pet,
        time = time,
        form = form)

@sarpi.route('/createpdf/<dateS>/<dateF>')
@login_required
def createpdf(dateS, dateF):
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    dateStart = datetime.strptime(dateS, '%Y-%m-%d').date()
    dateFinish = datetime.strptime(dateF, '%Y-%m-%d').date()

    schedules = Schedule.query.filter(Schedule.date_start >= dateStart, Schedule.date_start <= dateFinish ).filter_by(state = 'done').order_by(Schedule.date_start)

    create_pdf(render_template('template_pdf.html', schedules = schedules, time = time))

    return send_from_directory(PDF_DOWNLOAD,
        'file.pdf',
        as_attachment=True)

@sarpi.route('/weightreport/<dateS>/<dateF>')
@login_required
def weight_report(dateS, dateF):
    pet = Pet.query.get(1)
    time = datetime.now().strftime("%d-%m-%Y | %H:%M")

    dateStart = datetime.strptime(dateS, '%Y-%m-%d').date()
    dateFinish = datetime.strptime(dateF, '%Y-%m-%d').date()

    weights = PetWeight.query.filter(PetWeight.date_creation >= dateStart, PetWeight.date_creation <= dateFinish)

    return render_template('weight_report.html',
        tile = 'Weight History',
        pet = pet,
        time = time,
        weights = weights)