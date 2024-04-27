"""
Blueprinty logowania do systemu
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import MyForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Logowanie uzytkownika
    """
    if request.method =='POST':
        email = request.form.get('email') # moze zmienic na indetifikator czy cos
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Zalogowano', category='success')
                login_user(user, remember=True) # remember pamieta ze uzytkownik jest zalogowany ze strony serwera
                return redirect(url_for('views.home'))
            else:
                flash('Złe hasło', category='error')
        else:
           flash('Użytkownik nie istnieje', category='error') 
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """Wylogowuje i przekierowuje do logowania
    """
    
    logout_user()
    flash('Wylogowano', category='success') 
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    """Funkcja rejestracji uzytkownika
    
    Return: html remplate i argument user do wykorzystania w html
    """


    if request.method =='POST':
        
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Podany email jest przypisany do innego konta', category='error') 
        elif password1 != password2:
            flash('Hasła muszą być takie same', category='error')
            
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Rejestracja udana',category='success')
            return redirect(url_for('views.home'))
            
            
    return render_template("sign-up.html", user=current_user)
