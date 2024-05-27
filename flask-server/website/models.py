from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path 
from PIL import Image

user_patient = db.Table('user_patient', 
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
                        db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')))

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
    surname = db.Column(db.String(50))
    phonenumber = db.Column(db.Integer())
    specialization = db.Column(db.String(50))
    about = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    # address =  db.Column(db.String(50))
    
    patient = db.relationship('Patient', secondary=user_patient, backref='patients')
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
