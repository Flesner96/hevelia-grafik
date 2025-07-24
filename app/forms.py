from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class DodajPracownikaForm(FlaskForm):
    imie = StringField("Imię", validators=[DataRequired()])
    nazwisko = StringField("Nazwisko", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    haslo = PasswordField("Hasło", validators=[DataRequired(), Length(min=6)])
    rola = SelectField("Rola", choices=[
        ("recepcja", "Recepcja"),
        ("saunamistrz", "Saunamistrz"),
        ("bar", "Bar")
    ])
    submit = SubmitField("Dodaj pracownika")