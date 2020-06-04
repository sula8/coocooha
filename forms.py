from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField, PasswordField, BooleanField
from wtforms.validators import Length, InputRequired


class RegistrationForm(FlaskForm):
    email = StringField("Ваш email", [Length(min=1, max=25), InputRequired(message="Напишите свой email")])
    password = PasswordField("Ваш пароль", [Length(min=1, max=25), InputRequired(message="Напишите свой пароль")])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = StringField("Ваш email", [Length(min=1, max=25), InputRequired(message="Напишите свой email")])
    password = PasswordField("Ваш пароль", [Length(min=1, max=25), InputRequired(message="Напишите свой пароль")])
    submit = SubmitField("Войти")


class WizardForm(FlaskForm):
    ingredient = BooleanField()
    submit = SubmitField("Поехали!")
