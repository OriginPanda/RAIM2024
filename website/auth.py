"""
Blueprinty logowania do systemu
"""
from flask import Blueprint, render_template, request, flash

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
        name_id = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Hasła muszą być takie same', category='error')
            
        else:
            #TODO add user  
            flash('Rejestracja udana',category='success')
            pass
    return render_template("sign-up.html")