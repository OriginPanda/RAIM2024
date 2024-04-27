from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path 
from PIL import Image

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    #data_id = db.Column(db.Integer, db.ForeignKey('medical_data.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    imagename = db.Column(db.String(500))

class MedicalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    diagnosis = db.Column(db.String(), nullable=True)
    #comments = db.relationship('Comment')
    
    ## Placeholders
    filename = db.Column(db.String(500))
    
    #TODO dodac reszte danych
    
    # Opinion = db.Column(db.String(1000))
    # treatment = db.Column(db.String(1000))
    # nie wiem co dodać

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    # second_name = db.Column(db.String(50))
    # address =  db.Column(db.String(50))
    # phone_number = db.Column(db.Integer)
    
    comments = db.relationship('Comment')
    medicalDataAdded = db.relationship('MedicalData')
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    pesel = db.Column(db.Integer, unique=True)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    medicalRecord = db.relationship('MedicalData') #TODO zmiana na medical_record jak baza danych sie ogarnie
    opinions = db.relationship('Comment')
