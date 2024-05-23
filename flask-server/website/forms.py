from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField , SubmitField, IntegerField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email, ValidationError, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


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
       
class SettingsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message=("Wpisz email")),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])

    name =  StringField('Name')
    submit = SubmitField("Change")
       
def FileSizeLimit(max_size_in_mb):
        max_bytes = max_size_in_mb*1024*1024
        
        def file_length_check(form, field):
            if field.data:
                if len(field.data.read()) > max_bytes:
                    raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
                field.data.seek(0)
        return file_length_check       
        
FILE_TYPES = set(['png','jpeg','bmp']) 
class MedDataForm(FlaskForm):  
    
    
    title = StringField('Tytuł', validators=[DataRequired()])
    #patient_id = IntegerField('Id Pacjenta',validators=[DataRequired()])#,render_kw={'disabled':''} moze sie przydać
    text = StringField('Komentarz', validators=[DataRequired(),Length(max=500,message="Wiadomość za długa")], widget=TextArea(),render_kw={'class': 'form-control'})
    
    
    
    
    file = FileField('Dodaj Plik',validators=[FileSizeLimit(max_size_in_mb=1)])
    # def validate_file(form, field):
    #     if field.data != None:
    #         filename = field.data
    #         if '.' in filename and filename.rsplit('.', 1)[1]in FILE_TYPES:
    #             raise ValidationError("Zły rodzaj pliku")
        
    submit = SubmitField("Dodaj dane medyczne")
    
class CommentForm(FlaskForm):  
    
    
    text = StringField('Komentarz', validators=[DataRequired(),Length(max=500,message="Wiadomość za długa")], widget=TextArea(),render_kw={'class': 'form-control'})
    
        
    submit = SubmitField("Dodaj komentarz")