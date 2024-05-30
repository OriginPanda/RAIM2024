from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path 
from PIL import Image

# Tabela asocjacyjna do relacji wiele-do-wielu między użytkownikami a pacjentami
user_patient = db.Table(
    'user_patient', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'))
)

class Comment(db.Model):
    """
    Model reprezentujący komentarze do danych medycznych lub pacjentów.

    Atrybuty:
        id (int): Unikalny identyfikator komentarza.
        text (str): Treść komentarza, maksymalnie 500 znaków.
        date (datetime): Data i czas dodania komentarza.
        patient_id (int): Identyfikator pacjenta, do którego odnosi się komentarz.
        user_id (int): Identyfikator użytkownika, który dodał komentarz.
        imagename (str): Nazwa pliku obrazka związanego z komentarzem.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # data_id = db.Column(db.Integer, db.ForeignKey('medical_data.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    imagename = db.Column(db.String(500))

class MedicalData(db.Model):
    """
    Model reprezentujący dane medyczne pacjentów.

    Atrybuty:
        id (int): Unikalny identyfikator danych medycznych.
        title (str): Tytuł danych medycznych, maksymalnie 500 znaków.
        patient_id (int): Identyfikator pacjenta, do którego odnoszą się dane medyczne.
        user_id (int): Identyfikator użytkownika, który dodał dane medyczne.
        date (datetime): Data i czas dodania danych medycznych.
        diagnosis (str): Diagnoza związana z danymi medycznymi.
        filename (str): Nazwa pliku związanego z danymi medycznymi.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    diagnosis = db.Column(db.String(), nullable=True)
    # comments = db.relationship('Comment')
    
    # Placeholder dla nazwy pliku
    filename = db.Column(db.String(500))
    
    # TODO: dodac reszte danych, np.:
    # Opinion = db.Column(db.String(1000))
    # treatment = db.Column(db.String(1000))

class User(db.Model, UserMixin):
    """
    Model reprezentujący użytkowników systemu.

    Atrybuty:
        id (int): Unikalny identyfikator użytkownika.
        email (str): Adres email użytkownika, musi być unikalny.
        password (str): Hasło użytkownika.
        name (str): Imię użytkownika.
        surname (str): Nazwisko użytkownika.
        phonenumber (int): Numer telefonu użytkownika.
        specialization (str): Specjalizacja użytkownika.
        about (str): Opis użytkownika.
        picture (str): Nazwa pliku ze zdjęciem użytkownika.
        date_added (datetime): Data i czas dodania użytkownika.
        patient (list): Lista pacjentów powiązanych z użytkownikiem.
        comments (list): Lista komentarzy dodanych przez użytkownika.
        medicalDataAdded (list): Lista danych medycznych dodanych przez użytkownika.
    """
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
    """
    Model reprezentujący pacjentów.

    Atrybuty:
        id (int): Unikalny identyfikator pacjenta.
        name (str): Imię pacjenta.
        pesel (int): Numer PESEL pacjenta, musi być unikalny.
        date_added (datetime): Data i czas dodania pacjenta.
        medicalRecord (list): Lista danych medycznych powiązanych z pacjentem.
        opinions (list): Lista komentarzy dotyczących pacjenta.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    pesel = db.Column(db.Integer(), unique=True)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    medicalRecord = db.relationship('MedicalData')
    opinions = db.relationship('Comment')
