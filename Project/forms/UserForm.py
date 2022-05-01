import wtforms.fields
from wtforms.validators import DataRequired

from Project.forms.Form import Form


class LoginForm(Form):
    email = wtforms.EmailField('Почта', validators=[DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[DataRequired()])
