"""
Blueprinty logowania do systemu
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "LOGOWANIE"


@auth.route('/logout')
def logout():
    return "WYLOGOWANIE"


# @auth.route('/signup')
# def signup():
#     return "Rejestracja"