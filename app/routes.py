from calendar import monthrange
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app.models import ScheduleMonth, Shift, Uzytkownik
from app import db
from app.forms import DodajPracownikaForm

# Blueprint
main = Blueprint('main', __name__)

# Dashboard (dostępny dla każdego zalogowanego użytkownika)
@main.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Lista pracowników – tylko dla managera
@main.route('/pracownicy')
@login_required
def pracownicy():
    if current_user.rola != 'manager':
        flash("Nie masz dostępu do tej strony.", "error")
        return redirect(url_for('main.dashboard'))

    pracownicy = Uzytkownik.query.filter(Uzytkownik.rola != 'manager').all()
    return render_template('pracownicy.html', pracownicy=pracownicy)

# Dodawanie pracownika – tylko dla managera
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

@main.route("/grafiki")
@login_required
def grafiki():
    if current_user.rola != "manager":
        flash("Brak dostępu", "error")
        return redirect(url_for("main.dashboard"))

    today = date.today()
    current_month = today.month
    current_year = today.year

    # sprawdź, czy istnieje grafik na obecny miesiąc
    schedule = ScheduleMonth.query.filter_by(month=current_month, year=current_year).first()
    shifts = []
    days_in_month = monthrange(current_year, current_month)[1]

    if schedule:
        shifts = Shift.query.filter_by(schedule_id=schedule.id).all()

    return render_template("grafiki.html", schedule=schedule, shifts=shifts,
                           current_year=current_year, current_month=current_month, 
                           days=range(1, days_in_month+1))


@main.route("/stworz-grafik", methods=["POST"])
@login_required
def stworz_grafik():
    if current_user.rola != "manager":
        return redirect(url_for("main.dashboard"))

    today = date.today()
    year, month = today.year, today.month

    # zapobiegaj duplikacji
    existing = ScheduleMonth.query.filter_by(year=year, month=month).first()
    if existing:
        flash("Grafik już istnieje.", "info")
        return redirect(url_for("main.grafiki"))

    grafik = ScheduleMonth(year=year, month=month)
    db.session.add(grafik)
    db.session.commit()

    flash("Grafik utworzony. Teraz możesz go wypełnić.", "success")
    return redirect(url_for("main.grafiki"))

@main.route("/opublikuj-grafik/<int:schedule_id>", methods=["POST"])
@login_required
def opublikuj_grafik(schedule_id):
    if current_user.rola != "manager":
        return redirect(url_for("main.dashboard"))

    schedule = ScheduleMonth.query.get_or_404(schedule_id)
    schedule.is_published = True
    db.session.commit()
    flash("Grafik został opublikowany", "success")
    return redirect(url_for("main.grafiki"))

@main.route('/grafik/zapisz/<int:schedule_id>', methods=['POST'])
@login_required
def zapisz_grafik(schedule_id):
    schedule = ScheduleMonth.query.get_or_404(schedule_id)
    if schedule.is_published:
        flash("Grafik został już opublikowany.")
        return redirect(url_for('main.grafik'))

    data = request.form.getlist('shifts')
    for pracownik_id_str, dni in request.form.get('shifts', {}).items():
        pracownik_id = int(pracownik_id_str)
        for data_str, godziny in dni.items():
            shift_date = date.fromisoformat(data_str)
            godziny = godziny.strip()

            # szukamy istniejącej zmiany
            shift = Shift.query.filter_by(
                employee_id=pracownik_id,
                schedule_id=schedule_id,
                date=shift_date
            ).first()

            if godziny:
                if shift:
                    shift.shift_time = godziny
                else:
                    shift = Shift(
                        employee_id=pracownik_id,
                        schedule_id=schedule_id,
                        date=shift_date,
                        shift_time=godziny
                    )
                    db.session.add(shift)
            else:
                if shift:
                    db.session.delete(shift)

    db.session.commit()
    flash("Grafik zapisany.")
    return redirect(url_for('main.grafik'))