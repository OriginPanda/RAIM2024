from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    data_id = db.Column(db.Integer, db.ForeignKey('medical_data.id'))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class MedicalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment')
    
    
    #TODO dodac reszte danych
    data = None
    thumbnail = None
    category = None
    
    
    # nie wiem co dodać

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    comments = db.relationship('Comment')
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = first_name = db.Column(db.String(50))
    medicalRecord = db.relationship('MedicalData')
    
