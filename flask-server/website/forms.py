from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField 
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField 
from wtforms.validators import InputRequired 




class MyForm(FlaskForm): 
    name = StringField('Name', validators=[InputRequired()]) 
    password = PasswordField('Password', validators=[InputRequired()]) 
    remember_me = BooleanField('Remember me') 
    salary = DecimalField('Salary', validators=[InputRequired()]) 
    gender = RadioField('Gender', choices=[ ('male', 'Male'), ('female', 'Female')]) 
    message = TextAreaField('Message', validators=[InputRequired()]) 
    photo = FileField('Photo') 