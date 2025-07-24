from flask_login import UserMixin
from app import db

class Uzytkownik(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    nazwisko = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    haslo_hash = db.Column(db.String(200), nullable=False)
    rola = db.Column(db.String(50), nullable=False)

