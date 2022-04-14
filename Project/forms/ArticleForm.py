from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    heading = wtforms.StringField("heading", validators=[DataRequired()])

    def __init__(self, model: object = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model is not None:
            print(f"{model=}")
            model_keys = model.__dict__.keys()
            print(f"{model.__dict__['_sa_instance_state'].__dict__=}")
            print(f"{vars(model)}")
            for i in self.__dict__:
                print(f"{i=}, {model_keys=}")
                if i in model_keys:
                    self.__dict__[i].data = model.__dict__[i]
                    print(f"{model.__dict__[i]=}")
                    # setattr(self, i, model.__dict__[i])
