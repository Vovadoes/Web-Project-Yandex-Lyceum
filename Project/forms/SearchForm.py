from wtforms import StringField, SubmitField

from Project.forms.Form import Form


class SearchForm(Form):
    query = StringField("query")
    search = SubmitField("search")
    score = SubmitField("score")
