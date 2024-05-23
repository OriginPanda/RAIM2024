from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SettingsForm

from . import db


settings = Blueprint("settings", __name__)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings ():
    form = SettingsForm()
    if form.validate_on_submit():

        email = current_user.email 


        user = User.query.filter_by(email = email).first()
        user.name = form.name.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
    return render_template("settings.html", user=current_user, form=form)