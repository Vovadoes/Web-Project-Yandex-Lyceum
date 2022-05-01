from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = wtforms.EmailField('Почта', validators=[DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[DataRequired()])
