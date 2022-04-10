import wtforms
from wtforms.validators import DataRequired

from Project.forms.Form import Form


class TextForm(Form):
    heading = wtforms.StringField("heading", validators=[DataRequired()])
    text = wtforms.StringField("text", validators=[DataRequired()])
