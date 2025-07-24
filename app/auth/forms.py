from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    haslo = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")
