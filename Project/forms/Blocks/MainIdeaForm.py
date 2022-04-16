import wtforms
from wtforms.validators import DataRequired

from Project.forms.Form import Form


class MainIdeaForm(Form):
    idea = wtforms.StringField("Idea", validators=[DataRequired()])
