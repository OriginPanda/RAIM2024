"""
Blueprinty konkretnych widokow na stonie
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
views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
            
    patients = Patient.query.order_by(Patient.id)
    users = User.query.order_by(User.id)
    meddata = MedicalData.query.order_by(desc(MedicalData.date)).limit(4)
    return render_template("home.html", user=current_user, patients = patients, meddata = meddata, users = users)

@views.route('/com/delete', methods=['POST'])
@login_required
def delete_com():
    comment = json.loads(request.data)
    commentId = comment['commentId']
    comment = Comment.query.get(commentId)
    if comment:
        if comment.user_id == current_user.id:
            db.session.delete(comment)
            db.session.commit()
     
    return jsonify({})

@views.route('/patients', methods=['GET','POST'])
@login_required
def patients():
    form = PatientForm()   
    search = SearchField()
    if form.validate_on_submit():     
        patient = Patient.query.filter_by(pesel = form.pesel.data).first()
        if patient is None:
            patient = Patient(name=form.name.data, pesel=form.pesel.data)
            db.session.add(patient)
            db.session.commit()
            flash('Dodano pacjenta',category='success')
            form.data.clear()
            return redirect(url_for('views.patients'))
        else:
            form.pesel.errors.append("Użytkownik o podanym peselu już istnieje") 

    if search.validate_on_submit():     
        if search.searchResult.data:
            patients = Patient.query.filter(or_(Patient.pesel.like(search.searchResult.data), Patient.name.like(search.searchResult.data)))
        else:
            patients = Patient.query.order_by(Patient.id) 

         


    return render_template("patients.html", user = current_user, form = form, patients = patients, search=search)
            
    #return render_template("home.html", user=current_user)
    
@views.route('/patients/<int:patientId>', methods=['GET','POST'])
@login_required
def patientView(patientId):
    users = User.query.order_by(User.id)
    patient = Patient.query.get_or_404(patientId)
    #if current_user.group_id != patient.group_id 
    #else
    medform = MedDataForm()
    comform = CommentForm()
    
             
    return render_template("patient_profile.html",user = current_user, users = users, medform = medform, patient = patient, comform = comform)


@views.route('/patients/delete', methods=['POST'])
@login_required
def delete_patient():
    patient = json.loads(request.data)
    patientId = patient['patientId']
    patient = Patient.query.get_or_404(patientId)
    if patient:
        for meddata in patient.medicalRecord:
            db.session.delete(meddata)
        for opinion in patient.opinions:
            db.session.delete(opinion)
        #if patient.group_id == current_user.group_id:
        db.session.delete(patient)
        db.session.commit()
     
    return jsonify({})
@views.route('/patients/addToMyPatients', methods=['GET','POST'])
@login_required
def addToMyPatients():
    patient = json.loads(request.data)
    patientId = patient['patientId']
    patient = Patient.query.get_or_404(patientId)
    user = User.query.filter_by(id=current_user.id).first()
    user.patient.append(patient)

    db.session.commit()
    return jsonify({})

@views.route('/patients/deleteFromMyPatients', methods=['GET','POST'])
@login_required
def deleteFromMyPatients():
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
    
    patient = Patient.query.get_or_404(patientId)
    #if current_user.group_id != patient.group_id 
    #else
    users = User.query.order_by(User.id)  
    medform = MedDataForm()
    comform = CommentForm()
    
    if medform.submit.data and medform.validate_on_submit():
            # new_meddata = MedicalData(diagnosis=medform.text, user_id=current_user.id, patient_id = patientId, title=medform.title)
            filename = ''
            request.files['file'] # z jakiegoś powodu trzeba odpalić request po prostu i wtedy dopiero działa
            
            if medform.file.data:
                file = request.files['file'] 
                filename = secure_filename(file.filename)
                
                print(os.path.join(app.config['IMAGE_UPLOADS'], filename))
                medform.file.data.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
                
                
            #image.save(path.join(app.config["IMAGE_UPLOADS"], filename))
            print(filename)
            new_meddata = MedicalData(diagnosis=medform.text.data, user_id=current_user.id, patient_id = patientId, title=medform.title.data, filename = filename)
            db.session.add(new_meddata)
            db.session.commit()
            medform.data.clear()
            flash('Dodano dane', category='success')
            return redirect('/patients/'+str(patientId))

         
    return render_template("patient_profile.html", user = current_user, users = users, medform = medform, patient = patient, comform = comform)

@views.route('/patients/delMed', methods=['POST'])
@login_required
def deleteMedData():
    
    medicaldata = json.loads(request.data)
    medicaldataId = medicaldata['medicaldataId']
    medicaldata = MedicalData.query.get_or_404(medicaldataId)
    if medicaldata:
        print("2")
        if(current_user.id != medicaldata.user_id):
            return redirect(url_for('views.deleteMedData'))
        if medicaldata.filename:
            os.remove(os.path.join(app.config['IMAGE_UPLOADS'], medicaldata.filename))
            print(os.path.join(app.config['IMAGE_UPLOADS'], medicaldata.filename))
        #if medicaldata.group_id == current_user.group_id:
        db.session.delete(medicaldata)
        db.session.commit()
     
    return jsonify({})



@views.route('/patients/addCom/<int:patientId>', methods=['POST'])
@login_required
def addPatCom(patientId):
    
    patient = Patient.query.get_or_404(patientId)
    #if current_user.group_id != patient.group_id 
    #else
    users = User.query.order_by(User.id)
    medform = MedDataForm()
    comform = CommentForm()
    

    if comform.validate_on_submit():
        new_comment = Comment(text=comform.text.data, user_id=current_user.id, patient_id = patientId)
        db.session.add(new_comment)
        db.session.commit()
        comform.data.clear()
        flash('Dodano', category='success')
        return redirect('/patients/'+str(patientId))
             
    return render_template("patient_profile.html", user = current_user, users = users, medform = medform, patient = patient, comform = comform)

@views.route('/com/add', methods=['POST'])
@login_required
def addCom():
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
    meddata = MedicalData.query.get_or_404(meddataId)
    patient = Patient.query.get_or_404(meddata.patient_id)
    users = User.query.order_by(User.id)
    return render_template("meddata.html", user = current_user, users = users,  patient = patient, meddata = meddata)


# @views.route('/settings/change', methods=['POST'])
# @login_required
# def changeUserData():
    
#     user = User.query.order_by(current_user)  
#     form = UserForm()
    
#     if form.submit.data and form.validate_on_submit():
#             # new_meddata = MedicalData(diagnosis=medform.text, user_id=current_user.id, patient_id = patientId, title=medform.title)
#             picture = ''
#             request.files['file'] # z jakiegoś powodu trzeba odpalić request po prostu i wtedy dopiero działa
            
#             if form.picture.data:
#                 file = request.files['file'] 
#                 picture = secure_filename(file.picture)
                
#                 print(os.path.join(app.config['IMAGE_UPLOADS'], picture))
#                 form.file.data.save(os.path.join(app.config['IMAGE_UPLOADS'], picture))
                
#             user
#             #image.save(path.join(app.config["IMAGE_UPLOADS"], filename))
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