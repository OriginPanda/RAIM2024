from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app as app
from flask_login import login_required, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SettingsForm, UserForm
from werkzeug.utils import secure_filename
from . import db
import os 

settings = Blueprint("settings", __name__)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings ():
    form = SettingsForm()
    user_form = UserForm()
    user = current_user
    if form.validate_on_submit() and form.submit.data:
        print("1")
        user = User.query.get_or_404(current_user.id)
        user.password = generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
        
        flash('Zmiana Hasła udana',category='success')
        form.data.clear()
    if user_form.submit.data and user_form.validate_on_submit():
        filename = ''
        request.files['picture'] # z jakiegoś powodu trzeba odpalić request po prostu i wtedy dopiero działa
        if user_form.name.data:
            user.name =user_form.name.data
        if user_form.surname.data:
            user.surname = user_form.surname.data  
        if user_form.specialization.data:
            user.specialization = user_form.specialization.data
        if user_form.about.data:
            user.about = user_form.about.data
        if user_form.phonenumber.data:
            user.phonenumber = user_form.phonenumber.data
        if user_form.picture.data:
            file = request.files['picture'] 
            filename = secure_filename(file.filename)
            
            print(os.path.join(app.config['IMAGE_UPLOADS'], filename))
            user_form.picture.data.save(os.path.join(app.config['IMAGE_UPLOADS'],filename))
            user.picture = filename
            
            
        #image.save(path.join(app.config["IMAGE_UPLOADS"], filename))
        print(filename)
        db.session.commit()
        flash('Zmieniono dane', category='success')
        return redirect('/')
    return render_template("settings.html", user=current_user, form=form, user_form = user_form)