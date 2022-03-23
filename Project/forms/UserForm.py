from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = wtforms.EmailField('Почта', validators=[DataRequired()])
    age = wtforms.IntegerField("Возраст")
    position = wtforms.StringField("position")
    speciality = wtforms.StringField("Специальность")
    address = wtforms.StringField("Адрес")
    password = wtforms.PasswordField('Пароль', validators=[DataRequired()])
    remember_me = wtforms.BooleanField('Запомнить меня', )
    submit = wtforms.SubmitField('Войти')
