from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SubmitField, IntegerField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email, ValidationError




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
    
class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message=("Halo?"))])
    pesel = IntegerField('Pesel', validators=[DataRequired()])
    submit = SubmitField("Dodaj")
    
    def validate_pesel(form, field):
        check = str(field.data)
        if len(check) != 11:
            raise ValidationError("Błędny pesel")
     