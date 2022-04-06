from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    heading = wtforms.StringField("heading", validators=[DataRequired()])

    def __init__(self, model: object = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model is not None:
            model_keys = model.__dict__.keys()
            for i in self.__dict__:
                if i in model_keys:
                    self.__dict__[i].data = model.__dict__[i]
                    # setattr(self, i, model.__dict__[i])
