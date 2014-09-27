from sarpi import db

# Table with Pet Data
class Pet(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(30), nullable = False)
    type_pet = db.Column(db.String(10), nullable = False)
    url_image = db.Column(db.String(200), unique = True, nullable = False)

    # Relations
    weights = db.relationship('PetWeight', backref = 'pet', lazy='dynamic')
    schedules = db.relationship('Schedule', backref = 'pet', lazy='dynamic')

    def __repr__(self):
        return '<Pet %r>' % self.name

# Table with all weights of the pets
class PetWeight(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key = True, unique = True)
    date_creation = db.Column(db.Date, nullable = False)
    weight = db.Column(db.Float, nullable = False)

    # Foreing Keys
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable = False)

    def __repr__(self):
        return '<Weight %r>' % self.weight

# Table with owner data
class Owner(db.Model):

    # Columns
    username = db.Column(db.String(10), primary_key = True, unique = True)
    password = db.Column(db.String(10), nullable = False)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    # Relations
    schedules = db.relationship('Schedule', backref = 'owner', lazy='dynamic')

    # Def for login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<Owner %r>' % self.username

# IMPORTANT TABLE: Table with the feeding schedules of SARpi
class Schedule(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key = True, unique = True)
    description = db.Column(db.String(30), nullable = False)
    date_start = db.Column(db.Date, nullable = False)
    time_start = db.Column(db.Time, nullable = False)
    portion = db.Column(db.Integer, nullable = False)
    state = db.Column(db.String(10), nullable = False, index = True, default = 'to_do')

    #Foreing Keys
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable = False)
    owner_username = db.Column(db.Integer, db.ForeignKey('owner.username'), nullable = False)

    def __repr__(self):
        return '<Schedule %r>' % self.description

