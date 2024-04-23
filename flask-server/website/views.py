"""
Blueprinty konkretnych widokow na stonie
"""
import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Comment, Patient
from .forms import PatientForm
from . import db



views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method =='POST':
        comment = request.form.get('comment')
        if len(comment) < 1:
            flash('Nie zostało nic wpisane', category='error')
        else:
            new_comment = Comment(text=comment, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Dodano', category='success')
            
    return render_template("home.html", user=current_user)

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

@views.route('/patients/delete', methods=['POST'])
@login_required
def delete_patient():
    patient = json.loads(request.data)
    patientId = patient['patientId']
    patient = Patient.query.get(patientId)
    if patient:
        #if patient.group_id == current_user.group_id:
        db.session.delete(patient)
        db.session.commit()
     
    return jsonify({})