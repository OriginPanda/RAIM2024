from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path 
from PIL import Image

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    data_id = db.Column(db.Integer, db.ForeignKey('medical_data.id'))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    imagepath = db.Column(db.String(1000))

class MedicalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment')
    
    ## Placeholders
    data_url = None #db.Column()
    
    #TODO dodac reszte danych
    
    # Opinion = db.Column(db.String(1000))
    # treatment = db.Column(db.String(1000))
    # nie wiem co dodać

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    
    # second_name = db.Column(db.String(50))
    # address =  db.Column(db.String(50))
    # phone_number = db.Column(db.Integer)
    
    comments = db.relationship('Comment')
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    medicalRecord = db.relationship('MedicalData')
    
