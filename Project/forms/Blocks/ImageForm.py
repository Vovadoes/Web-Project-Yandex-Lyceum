import wtforms
from wtforms.validators import DataRequired

from Project.forms.Form import Form


class ImageForm(Form):
    heading = wtforms.StringField("heading", validators=[])
