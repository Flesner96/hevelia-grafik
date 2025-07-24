from flask_login import UserMixin
from app import db
from datetime import datetime, date

class Uzytkownik(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    nazwisko = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    haslo_hash = db.Column(db.String(200), nullable=False)
    rola = db.Column(db.String(50), nullable=False)
    
    shifts = db.relationship('Shift', backref='employee', cascade='all, delete-orphan')

class ScheduleMonth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shifts = db.relationship('Shift', backref='schedule', cascade='all, delete-orphan')

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('uzytkownik.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule_month.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    shift_time = db.Column(db.String(50), nullable=False)  # np. "8:00–16:00"
