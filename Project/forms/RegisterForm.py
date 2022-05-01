from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
