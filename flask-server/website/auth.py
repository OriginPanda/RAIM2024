"""
Blueprinty logowania do systemu
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Logowanie uzytkownika
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data # moze zmienic na indetifikator czy cos
        password = form.password.data
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Zalogowano', category='success')
                login_user(user, remember=form.remember.data) # remember pamieta ze uzytkownik jest zalogowany ze strony serwera
                print(form.remember.data)
                form.data.clear()
                return redirect(url_for('views.home'))
            else:
                form.password.errors.append("Złe hasło")
        else:
           form.email.errors.append("Użytkownik nie istnieje")
           form.password.errors.append("")
    
    
    return render_template("login.html", user=current_user, form = form)


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
 
    form = RegisterForm()     
    if form.validate_on_submit():     
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            user = User(email=form.email.data, name=form.name.data, password=generate_password_hash(form.password.data, method='sha256'))
            db.session.add(user)
            db.session.commit()
            flash('Rejestracja udana',category='success')
            form.data.clear()
            return redirect(url_for('auth.login'))
        else:
           form.email.errors.append("Użytkownik o podanym adresie istnieje")
    users = User.query.order_by(User.date_added)          
    return render_template("sign-up.html", user=current_user, form = form, users=users)

