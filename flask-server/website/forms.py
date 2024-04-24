from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SubmitField, IntegerField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email, ValidationError, Length




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
        
FILE_TYPES = set(['txt', 'doc', 'docx', 'odt', 'pdf', 'rtf', 'text', 'wks', 'wps', 'wpd','png','jpeg']) 
class MedDataForm(FlaskForm):  
    
    
    title = StringField('Tytuł', validators=[DataRequired()])
    #patient_id = IntegerField('Id Pacjenta',validators=[DataRequired()])#,render_kw={'disabled':''} moze sie przydać
    text = StringField('Komentarz', validators=[DataRequired(),Length(max=500,message="Wiadomość za długa")])
    file = FileField('Dodaj Plik')
    
    # def validate_file(form, field):
    #     if field.data:
    #         filename = str(field.data.filename)
    #         if '.' in filename and filename.rsplit('.', 1)[1]in FILE_TYPES:
    #             raise ValidationError("Zły rodzaj pliku")
        
    submit = SubmitField("Dodaj dane medyczne")
    
class CommentForm(FlaskForm):  
    
    
    title = StringField('Tytuł', validators=[DataRequired()])
    text = StringField('Komentarz', validators=[DataRequired(),Length(max=500,message="Wiadomość za długa")])
    
        
    submit = SubmitField("Dodaj komentarz")