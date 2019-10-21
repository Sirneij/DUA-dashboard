from app         import db
from flask_login import UserMixin

from . common    import COMMON, STATUS, DATATYPE

class User(UserMixin, db.Model):

    id          = db.Column(db.Integer,     primary_key=True)
    username    = db.Column(db.String(64), nullable= False)
    email       = db.Column(db.String(120), nullable=False, unique = True)
    firstName   = db.Column(db.String(500), nullable=False)
    lastName    = db.Column(db.String(500), nullable=False)
    about       = db.Column(db.String(20000))
    role        = db.Column(db.Integer)
    password    = db.Column(db.String(500), nullable=False)
    password_q  = db.Column(db.Integer)
    image_file  = db.Column(db.String(20), nullable=False, default='default.png')

    def __init__(self, username, password, firstName, email, lastName, about, image_file):
        self.username   = username
        self.password   = password
        self.password_q = DATATYPE.CRYPTED
        self.firstName  = firstName
        self.email      = email
        self.lastName   = lastName
        self.about      = about
        self.image_file = image_file

        self.group_id = None
        self.role     = None

    def __repr__(self):
        return f"User('{self.self.firstName}','{self.self.lastName}', '{self.username}', '{self.image_file}')"

    def save(self):

        # inject self into db session
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self
