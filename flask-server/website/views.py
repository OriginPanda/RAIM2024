"""
Blueprinty konkretnych widokow na stonie
"""
import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Comment, Patient
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

@views.route('/delete-com', methods=['POST'])
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
def patient():
    if request.method =='POST':
        data = request.form.get('data')
        if len(data) < 1:
            flash('Nie zostało nic wpisane', category='error')
        else:
            new_patient = Patient(first_name=data)

            db.session.add(new_patient)
            db.session.commit()
            flash('Dodano', category='success')
    return render_template("patients.html", user=current_user, patients = Patient.query.all())

