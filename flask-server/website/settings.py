from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


settings = Blueprint("settings", __name__)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def patientsettings ():
    return render_template("settings.html", user=current_user)
