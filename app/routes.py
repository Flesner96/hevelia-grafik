from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/dodaj-pracownika')
@login_required
def dodaj_pracownika():
    return "<h2>Tu będzie formularz dodawania pracownika</h2>"
