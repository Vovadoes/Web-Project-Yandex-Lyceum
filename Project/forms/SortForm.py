from wtforms import SubmitField

from Project.forms.Form import Form


class SortForm(Form):
    populated = SubmitField("Популярность")
    time = SubmitField("Время")
