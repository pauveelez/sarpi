from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed
from wtforms import TextField, BooleanField, PasswordField, SelectField, IntegerField, DateField, RadioField
from wtforms.validators import Required, Length, Regexp, Email, EqualTo

#Clases que definen los formularios de SARpi

class LoginForm(Form):
    username = TextField('Username', validators = [Required(), Length(min=5, max=10)])
    password = PasswordField('Password', validators = [Required(), Length(min=5, max=10)])

class EditFormPet(Form):
    name = TextField('Name', validators = [Required(), Length(min=3, max=30)])
    type_pet = TextField('Type Pet', validators = [Required(), Length(min=3, max=10)])
    weight = TextField('Weight',  validators = [Required(), Regexp('^[0-9]+(\.[0-9]{1})?$', message = 'Invalid Weight')])
    image = FileField('Pet Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])

class EditFormOwner(Form):
    name = TextField('Name', validators = [Required(), Length(min=3, max=30)])
    email = TextField('Email', validators = [Required(), Length(min=5, max=120), Email()])
    newPassword = PasswordField('New Password', validators = [EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

class ProgramSchedule(Form):
    description = TextField('Descripcion', validators = [Required(), Length(min=3, max=30)])
    portion  = IntegerField('Porcion', validators = [Required()])
    hours = SelectField('Horas', validators = [Required()])

class CreateReport(Form):
    dateStart = DateField('Fecha Inicio', format='%Y-%m-%d', validators = [Required()])
    dateFinish = DateField('Fecha Fin', format='%Y-%m-%d', validators = [Required()])
    type_report = RadioField('Tipo de Reporte', choices = [('1','Lista de Horarios Realizados'),('2','Historial de Pesos')], validators = [Required()])