from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import Uzytkownik
from app import db
from . import auth
from .forms import LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Uzytkownik.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.haslo_hash, form.haslo.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Błędny email lub hasło', 'error')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
