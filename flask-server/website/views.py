"""
Blueprinty konkretnych widokow na stonie
"""
import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app as app
from flask_login import login_required, current_user
from .models import Comment, Patient, MedicalData
from .forms import PatientForm, MedDataForm, CommentForm
from . import db
from os import path 
from werkzeug.utils import secure_filename


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    comform = CommentForm()
            
    return render_template("home.html", user=current_user, comform = comform)

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
    patients = Patient.query.order_by(Patient.id)          
    return render_template("patients.html", user = current_user, form = form, patients = patients)
            
    #return render_template("home.html", user=current_user)
    
@views.route('/patients/<int:patientId>', methods=['GET','POST'])
@login_required
def patientView(patientId):
    
    patient = Patient.query.get_or_404(patientId)
    #if current_user.group_id != patient.group_id 
    #else
    medform = MedDataForm()
    comform = CommentForm()
    
    if medform.submit.data and medform.validate_on_submit():
            # new_meddata = MedicalData(diagnosis=medform.text, user_id=current_user.id, patient_id = patientId, title=medform.title)
            new_meddata = MedicalData(diagnosis=medform.text.data, user_id=current_user.id, patient_id = patientId, title=medform.title.data)
            db.session.add(new_meddata)
            db.session.commit()
            medform.data.clear()
            flash('Dodano dane', category='success')
            return redirect('/patients/'+str(patientId))
        
    if comform.validate_on_submit():
        
        new_comment = Comment(text=comform.text.data, user_id=current_user.id, patient_id = patientId)
        db.session.add(new_comment)
        db.session.commit()
        comform.data.clear()
        flash('Dodano', category='success')
        return redirect('/patients/'+str(patientId))
             
    return render_template("patient_profile.html", user = current_user, medform = medform, patient = patient, comform = comform)


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

@views.route('/patients/addMed/<int:patientId>', methods=['POST'])
@login_required
def addPatMed(patientId):
    
    patient = Patient.query.get_or_404(patientId)
    #if current_user.group_id != patient.group_id 
    #else
    medform = MedDataForm()
    comform = CommentForm()
    
    if medform.submit.data and medform.validate_on_submit():
            # new_meddata = MedicalData(diagnosis=medform.text, user_id=current_user.id, patient_id = patientId, title=medform.title)
            filename = ''
            request.files['file'] # z jakiegoś powodu trzeba odpalić request po prostu i wtedy dopiero działa
            
            if medform.file.data:
                file = request.files['file'] 
                filename = secure_filename(file.filename)
                
                #print(secure_filename("siema.txt")) # nie wiem czemu nie działa
                
                print(path.join(app.config['IMAGE_UPLOADS'], filename))
                medform.file.data.save(path.join(app.config['IMAGE_UPLOADS'], filename))
            #image.save(path.join(app.config["IMAGE_UPLOADS"], filename))
            print(filename)
            new_meddata = MedicalData(diagnosis=medform.text.data, user_id=current_user.id, patient_id = patientId, title=medform.title.data, filename = filename)
            db.session.add(new_meddata)
            db.session.commit()
            medform.data.clear()
            flash('Dodano dane', category='success')
            return redirect('/patients/'+str(patientId))

         
    return render_template("patient_profile.html", user = current_user, medform = medform, patient = patient, comform = comform)

@views.route('/patients/delMed', methods=['POST'])
@login_required
def deleteMedData():
    medicaldata = json.loads(request.data)
    medicaldataId = medicaldata['medicaldataId']
    medicaldata = MedicalData.query.get_or_404(medicaldataId)
    if medicaldata:
        #if medicaldata.group_id == current_user.group_id:
        db.session.delete(medicaldata)
        db.session.commit()
     
    return jsonify({})


#TODO Do połączeniea addPacCom i addCom
@views.route('/patients/addCom/<int:patientId>', methods=['POST'])
@login_required
def addPatCom(patientId):
    
    patient = Patient.query.get_or_404(patientId)
    #if current_user.group_id != patient.group_id 
    #else
    medform = MedDataForm()
    comform = CommentForm()
    

    if comform.validate_on_submit():
        print('siema')
        new_comment = Comment(text=comform.text.data, user_id=current_user.id, patient_id = patientId)
        db.session.add(new_comment)
        db.session.commit()
        comform.data.clear()
        flash('Dodano', category='success')
        return redirect('/patients/'+str(patientId))
             
    return render_template("patient_profile.html", user = current_user, medform = medform, patient = patient, comform = comform)

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

