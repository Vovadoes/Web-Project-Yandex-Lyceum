from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class PasswordForm(FlaskForm):
    password = wtforms.fields.PasswordField('Пароль', validators=[DataRequired()])
    password_again = wtforms.fields.PasswordField('Повторите пароль', validators=[DataRequired()])
