"""
Blueprinty konkretnych widoków na stronie.
"""
import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app as app
from flask_login import login_required, current_user
from .models import Comment, Patient, MedicalData, User
from .forms import PatientForm, MedDataForm, CommentForm, UserForm, SearchField
from . import db
import os
from werkzeug.utils import secure_filename
from sqlalchemy import desc, or_

# Tworzenie blueprintu 'views' do obsługi widoków
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Widok strony głównej.

    Pobiera wszystkich pacjentów i użytkowników z bazy danych
    i renderuje stronę główną.
    """
    patients = Patient.query.order_by(Patient.id)
    users = User.query.order_by(User.id)
    return render_template("home.html", user=current_user, patients=patients, users=users)

@views.route('/com/delete', methods=['POST'])
@login_required
def delete_com():
    """
    Widok usuwania komentarza.

    Pobiera dane komentarza z żądania, usuwa go z bazy danych,
    jeśli użytkownik jest autorem komentarza.
    """
    comment = json.loads(request.data)
    commentId = comment['commentId']
    comment = Comment.query.get(commentId)
    if comment:
        if comment.user_id == current_user.id:
            db.session.delete(comment)
            db.session.commit()
    return jsonify({})

@views.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    """
    Widok zarządzania pacjentami.

    Umożliwia dodawanie nowych pacjentów oraz wyszukiwanie istniejących.
    """
    form = PatientForm()
    search = SearchField()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(pesel=form.pesel.data).first()
        if patient is None:
            patient = Patient(name=form.name.data, pesel=form.pesel.data)
            db.session.add(patient)
            db.session.commit()
            flash('Dodano pacjenta', category='success')
            form.data.clear()
            return redirect(url_for('views.patients'))
        else:
            form.pesel.errors.append("Użytkownik o podanym peselu już istnieje")
            
    patients = Patient.query.order_by(Patient.id)        

    if search.validate_on_submit():     
        if search.searchResult.data:
            patients = Patient.query.filter(
                or_(Patient.pesel.like(search.searchResult.data), Patient.name.like(search.searchResult.data))
            )
    return render_template("patients.html", user=current_user, form=form, patients=patients, search=search)

@views.route('/patients/<int:patientId>', methods=['GET', 'POST'])
@login_required
def patientView(patientId):
    """
    Widok szczegółów pacjenta.

    Wyświetla profil pacjenta, komentarze i dane medyczne.
    """
    users = User.query.order_by(User.id)
    patient = Patient.query.get_or_404(patientId)
    comments = Comment.query.filter_by(patient_id=patientId).order_by(desc(Comment.date))
    medicalRecord = MedicalData.query.filter_by(patient_id=patientId).order_by(desc(MedicalData.date))
    
    medform = MedDataForm()
    comform = CommentForm()
    
    return render_template("patient_profile.html", user=current_user, users=users, medform=medform, patient=patient, comform=comform, comments=comments, medicalRecord=medicalRecord)

@views.route('/patients/delete', methods=['POST'])
@login_required
def delete_patient():
    """
    Widok usuwania pacjenta.

    Usuwa pacjenta oraz powiązane z nim dane medyczne i komentarze.
    """
    patient = json.loads(request.data)
    patientId = patient['patientId']
    patient = Patient.query.get_or_404(patientId)
    if patient:
        for meddata in patient.medicalRecord:
            db.session.delete(meddata)
        for opinion in patient.opinions:
            db.session.delete(opinion)
        db.session.delete(patient)
        db.session.commit()
    return jsonify({})

@views.route('/patients/addToMyPatients', methods=['GET', 'POST'])
@login_required
def addToMyPatients():
    """
    Widok dodawania pacjenta do listy moich pacjentów.

    Dodaje wybranego pacjenta do listy pacjentów zalogowanego użytkownika.
    """
    patient = json.loads(request.data)
    patientId = patient['patientId']
    patient = Patient.query.get_or_404(patientId)
    user = User.query.filter_by(id=current_user.id).first()
    user.patient.append(patient)
    db.session.commit()
    return jsonify({})

@views.route('/patients/deleteFromMyPatients', methods=['GET', 'POST'])
@login_required
def deleteFromMyPatients():
    """
    Widok usuwania pacjenta z listy moich pacjentów.

    Usuwa wybranego pacjenta z listy pacjentów zalogowanego użytkownika.
    """
    patient = json.loads(request.data)
    patientId = patient['patientId']
    patient = Patient.query.get_or_404(patientId)
    user = User.query.filter_by(id=current_user.id).first()
    user.patient.remove(patient)
    db.session.commit()
    return jsonify({})

@views.route('/patients/MedData/add/<int:patientId>', methods=['POST'])
@login_required
def addPatMed(patientId):
    """
    Widok dodawania danych medycznych dla pacjenta.

    Dodaje nowe dane medyczne dla wybranego pacjenta.
    """
    patient = Patient.query.get_or_404(patientId)
    users = User.query.order_by(User.id)
    medform = MedDataForm()
    comform = CommentForm()
    
    if medform.submit.data and medform.validate_on_submit():
        filename = ''
        request.files['file']
        
        if medform.file.data:
            file = request.files['file']
            filename = secure_filename(file.filename)
            medform.file.data.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
        
        new_meddata = MedicalData(
            diagnosis=medform.text.data, user_id=current_user.id, patient_id=patientId, title=medform.title.data, filename=filename
        )
        db.session.add(new_meddata)
        db.session.commit()
        medform.data.clear()
        flash('Dodano dane', category='success')
        return redirect('/patients/' + str(patientId))
    
    return render_template("patient_profile.html", user=current_user, users=users, medform=medform, patient=patient, comform=comform)

@views.route('/patients/delMed', methods=['POST'])
@login_required
def deleteMedData():
    """
    Widok usuwania danych medycznych.

    Usuwa wybrane dane medyczne z bazy danych oraz powiązany plik.
    """
    medicaldata = json.loads(request.data)
    medicaldataId = medicaldata['medicaldataId']
    medicaldata = MedicalData.query.get_or_404(medicaldataId)
    if medicaldata:
        if current_user.id != medicaldata.user_id:
            return redirect(url_for('views.deleteMedData'))
        if medicaldata.filename:
            os.remove(os.path.join(app.config['IMAGE_UPLOADS'], medicaldata.filename))
        db.session.delete(medicaldata)
        db.session.commit()
    return jsonify({})

@views.route('/patients/addCom/<int:patientId>', methods=['POST'])
@login_required
def addPatCom(patientId):
    """
    Widok dodawania komentarza do pacjenta.

    Dodaje nowy komentarz do wybranego pacjenta.
    """
    patient = Patient.query.get_or_404(patientId)
    users = User.query.order_by(User.id)
    medform = MedDataForm()
    comform = CommentForm()
    
    if comform.validate_on_submit():
        new_comment = Comment(text=comform.text.data, user_id=current_user.id, patient_id=patientId)
        db.session.add(new_comment)
        db.session.commit()
        comform.data.clear()
        flash('Dodano', category='success')
        return redirect('/patients/' + str(patientId))
    
    return render_template("patient_profile.html", user=current_user, users=users, medform=medform, patient=patient, comform=comform)

@views.route('/com/add', methods=['POST'])
@login_required
def addCom():
    """
    Widok dodawania komentarza.

    Dodaje nowy komentarz.
    """
    comform = CommentForm()
    
    if comform.validate_on_submit():
        new_comment = Comment(text=comform.text.data, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/')
    
    return redirect('/')

@views.route('patients/MedData/<int:meddataId>')
@login_required
def viewMedData(meddataId):
    """
    Widok wyświetlania danych medycznych.

    Wyświetla szczegóły wybranych danych medycznych.
    """
    meddata = MedicalData.query.get_or_404(meddataId)
    patient = Patient.query.get_or_404(meddata.patient_id)
    users = User.query.order_by(User.id)
    return render_template("meddata.html", user=current_user, users=users, patient=patient, meddata=meddata)

# @views.route('/settings/change', methods=['POST'])
# @login_required
# def changeUserData():
    
#     user = User.query.order_by(current_user)
#     form = UserForm()
    
#     if form.submit.data and form.validate_on_submit():
#             picture = ''
#             request.files['file']
            
#             if form.picture.data:
#                 file = request.files['file']
#                 picture = secure_filename(file.picture)
                
#                 print(os.path.join(app.config['IMAGE_UPLOADS'], picture))
#                 form.file.data.save(os.path.join(app.config['IMAGE_UPLOADS'], picture))
                
#             user
#             print(picture)
#             user.name = form.name.data
#             user.surname = form.surname.data
#             user.specialization = form.specialization.data
#             user.description = form.description.data
#             user.contact = form.contact.data
#             user.email = form.email.data
            
#             db.session.commit()
#             flash('Dodano dane', category='success')
#             return redirect('/settings')

#     return redirect('/settings')
