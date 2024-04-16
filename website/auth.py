"""
Blueprinty logowania do systemu
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", var="Logowanie",)


@auth.route('/logout')
def logout():
    return "Wylogowano"


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if password1 != password2:
            flash('Hasła muszą być takie same', category='error')
            
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Rejestracja udana',category='success')
            return redirect(url_for('views.home'))
    return render_template("sign-up.html")