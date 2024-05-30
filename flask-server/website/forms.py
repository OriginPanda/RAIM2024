from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, validators
from wtforms import DecimalField, RadioField, SelectField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email, ValidationError, Length, Optional
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed
#from flask_uploads import UploadSet, IMAGES

class RegisterForm(FlaskForm):
    """
    Formularz rejestracyjny dla nowych użytkowników.

    Pola:
        name (StringField): Pole na imię z walidatorem wymagalności.
        password (PasswordField): Pole na hasło z walidatorem wymagalności.
        repassword (PasswordField): Pole do ponownego wpisania hasła z walidatorem równości z hasłem.
        email (StringField): Pole na email z walidatorem wymagalności i poprawności formatu email.
        submit (SubmitField): Przycisk wysyłania formularza.
    """
    name = StringField('Name', validators=[DataRequired(message=("Halo?"))])
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(message=("Wpisz email")), Email()])
    submit = SubmitField("Sign Up")
    
    # Zakomentowane pola, mogą być użyte w przyszłości:
    # remember_me = BooleanField('Remember me')
    # salary = DecimalField('Salary', validators=[InputRequired()])
    # gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    # message = TextAreaField('Message', validators=[InputRequired()])
    # photo = FileField('Photo')

class LoginForm(FlaskForm):
    """
    Formularz logowania.

    Pola:
        email (StringField): Pole na email z walidatorem wymagalności i poprawności formatu email.
        password (PasswordField): Pole na hasło z walidatorem wymagalności.
        remember (BooleanField): Pole wyboru do zapamiętania użytkownika.
        submit (SubmitField): Przycisk wysyłania formularza.
    """
    email = StringField('Email', validators=[DataRequired(message=("Wpisz email")), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember?')
    submit = SubmitField("Login")

class PatientForm(FlaskForm):
    """
    Formularz dla danych pacjenta.

    Pola:
        name (StringField): Pole na imię pacjenta z walidatorem wymagalności.
        pesel (IntegerField): Pole na numer PESEL pacjenta z walidatorem wymagalności.
        submit (SubmitField): Przycisk wysyłania formularza.
    
    Metody:
        validate_pesel (function): Własna walidacja dla pola PESEL.
    """
    name = StringField('Imie', validators=[DataRequired(message=("Halo?"))])
    pesel = IntegerField('Pesel', validators=[DataRequired()])
    submit = SubmitField("Dodaj")
    
    def validate_pesel(form, field):
        """
        Walidator dla numeru PESEL.
        
        Sprawdza, czy numer PESEL ma dokładnie 11 cyfr.

        Args:
            form (FlaskForm): Formularz, który zawiera pole.
            field (Field): Pole do walidacji.

        Raises:
            ValidationError: Jeśli numer PESEL nie ma dokładnie 11 cyfr.
        """
        check = str(field.data)
        if len(check) != 11:
            raise ValidationError("Błędny pesel")

def FileSizeLimit(max_size_in_mb):
    """
    Tworzy walidator sprawdzający, czy rozmiar pliku nie przekracza maksymalnego limitu.

    Args:
        max_size_in_mb (int): Maksymalny rozmiar pliku w megabajtach.

    Returns:
        function: Walidator sprawdzający rozmiar pliku.
    """
    max_bytes = max_size_in_mb * 1024 * 1024

    def file_length_check(form, field):
        """
        Sprawdza rozmiar pliku.

        Args:
            form (FlaskForm): Formularz, który zawiera pole.
            field (Field): Pole do walidacji.

        Raises:
            ValidationError: Jeśli rozmiar pliku przekracza maksymalny limit.
        """
        if field.data:
            if len(field.data.read()) > max_bytes:
                raise ValidationError(f"File size must be less than {max_size_in_mb}MB")
            field.data.seek(0)

    return file_length_check

# Dozwolone typy plików
FILE_TYPES = set(['png', 'jpeg', 'bmp'])

class MedDataForm(FlaskForm):
    """
    Formularz dla danych medycznych.

    Pola:
        title (StringField): Pole na tytuł z walidatorem wymagalności.
        text (StringField): Pole na diagnozę z walidatorem wymagalności i limitu długości oraz widżetem TextArea.
        file (FileField): Pole do dodawania pliku z limitem rozmiaru 1MB.
        submit (SubmitField): Przycisk wysyłania formularza.
    """
    title = StringField('Tytuł', validators=[DataRequired()])
    text = StringField('Diagnoza', validators=[DataRequired(), Length(max=500, message="Wiadomość za długa")], widget=TextArea(), render_kw={'class': 'form-control'})
    file = FileField('Dodaj Plik', validators=[FileSizeLimit(max_size_in_mb=1)])
    
    # Zakomentowane walidacje, mogą być użyte w przyszłości:
    # def validate_file(form, field):
    #     if field.data != None:
    #         filename = field.data
    #         if '.' in filename and filename.rsplit('.', 1)[1] in FILE_TYPES:
    #             raise ValidationError("Zły rodzaj pliku")

    submit = SubmitField("Dodaj dane medyczne")

class CommentForm(FlaskForm):
    """
    Formularz do dodawania komentarzy.

    Pola:
        text (StringField): Pole na komentarz z walidatorem wymagalności i limitu długości oraz widżetem TextArea.
        submit (SubmitField): Przycisk wysyłania formularza.
    """
    text = StringField('Komentarz', validators=[DataRequired(), Length(max=500, message="Wiadomość za długa")], widget=TextArea(), render_kw={'class': 'form-control'})
    submit = SubmitField("Dodaj komentarz")

class SettingsForm(FlaskForm):
    """
    Formularz ustawień użytkownika.

    Pola:
        password (PasswordField): Pole na hasło z walidatorem wymagalności.
        repassword (PasswordField): Pole do ponownego wpisania hasła z walidatorem równości z hasłem.
        submit (SubmitField): Przycisk wysyłania formularza.
    """
    # Zakomentowane pole na email, może być użyte w przyszłości:
    #email = StringField('Email', validators=[DataRequired(message=("Wpisz email")), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Change")

class UserForm(FlaskForm):
    """
    Formularz dla danych użytkownika.

    Pola:
        name (StringField): Pole na imię użytkownika.
        surname (StringField): Pole na nazwisko użytkownika.
        specialization (StringField): Pole na specjalizację użytkownika.
        about (StringField): Pole na opis użytkownika z walidatorem limitu długości oraz widżetem TextArea.
        phonenumber (IntegerField): Pole na numer telefonu z walidatorem opcjonalności.
        picture (FileField): Pole na zdjęcie z limitami rozmiaru i dozwolonymi typami plików.
        submit (SubmitField): Przycisk wysyłania formularza.

    Metody:
        validate_phonenumber (function): Własna walidacja dla numeru telefonu.
    """
    name = StringField('Imię')
    surname = StringField('Nazwisko')
    specialization = StringField('Specjalizacja')
    about = StringField('Opis', validators=[Length(max=1000, message="Opis zbyt długi")], widget=TextArea(), render_kw={'class': 'form-control'})
    phonenumber = IntegerField('Numer tel.', [validators.optional()])
    picture = FileField('Zdjęcie', validators=[FileSizeLimit(max_size_in_mb=5), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Zapisz zmiany')

    def validate_phonenumber(form, field):
        """
        Walidator dla numeru telefonu.

        Sprawdza, czy numer telefonu ma dokładnie 9 cyfr.

        Args:
            form (FlaskForm): Formularz, który zawiera pole.
            field (Field): Pole do walidacji.

        Raises:
            ValidationError: Jeśli numer telefonu nie ma dokładnie 9 cyfr.
        """
        if field.data != None:
            print(field.data)
            check = str(field.data)
            if len(check) != 9:
                raise ValidationError("Zły numer tel")

class SearchField(FlaskForm):
    """
    Formularz wyszukiwania.

    Pola:
        searchResult (StringField): Pole wyszukiwania z walidatorem opcjonalności.
        submit (SubmitField): Przycisk wysyłania formularza.
    """
    searchResult = StringField("Wyszukiwanie", validators=[Optional()])
    submit = SubmitField('Szukaj')
