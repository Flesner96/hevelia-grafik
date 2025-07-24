from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Uzytkownik
from app import db
from app.forms import DodajPracownikaForm
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/pracownicy')
@login_required
def pracownicy():
    if current_user.rola != 'manager':
        flash("Nie masz dostępu do tej strony.", "error")
        return redirect(url_for('main.dashboard'))
    
    pracownicy = Uzytkownik.query.filter(Uzytkownik.rola != 'manager').all()
    return render_template('pracownicy.html', pracownicy=pracownicy)

@main.route('/dodaj-pracownika', methods=['GET', 'POST'])
@login_required
def dodaj_pracownika():
    if current_user.rola != 'manager':
        flash("Nie masz dostępu.", "error")
        return redirect(url_for('main.dashboard'))

    form = DodajPracownikaForm()
    if form.validate_on_submit():
        istnieje = Uzytkownik.query.filter_by(email=form.email.data).first()
        if istnieje:
            flash("Użytkownik o takim e-mailu już istnieje.", "error")
            return redirect(url_for('main.dodaj_pracownika'))
        
        nowy = Uzytkownik(
            imie=form.imie.data,
            nazwisko=form.nazwisko.data,
            email=form.email.data,
            haslo_hash=generate_password_hash(form.haslo.data),
            rola=form.rola.data
        )
        db.session.add(nowy)
        db.session.commit()
        flash("Pracownik dodany!", "success")
        return redirect(url_for('main.pracownicy'))

    return render_template("dodaj_pracownika.html", form=form)