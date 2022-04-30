import wtforms
from wtforms.validators import DataRequired

from Project.forms.Form import Form


class CommentForm(Form):
    text = wtforms.StringField("Текст", validators=[DataRequired()])
