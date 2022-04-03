from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    heading = wtforms.StringField("heading", validators=[DataRequired()])

    submit = wtforms.SubmitField('Создать')
