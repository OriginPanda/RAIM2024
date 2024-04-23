from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SubmitField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email




class RegisterForm  (FlaskForm): 
    name = StringField('Name', validators=[DataRequired(message=("Halo?"))]) 
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(message=("Wpisz email")),Email()])
    submit = SubmitField("Sign Up")
    
    
    
    
     
    # remember_me = BooleanField('Remember me') 
    # salary = DecimalField('Salary', validators=[InputRequired()]) 
    # gender = RadioField('Gender', choices=[ ('male', 'Male'), ('female', 'Female')]) 
    # message = TextAreaField('Message', validators=[InputRequired()]) 
    # photo = FileField('Photo') 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message=("Wpisz email")),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember?')
    submit = SubmitField("Login")