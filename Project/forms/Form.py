from flask_wtf import FlaskForm
import wtforms.fields
from wtforms.validators import DataRequired


class Form(FlaskForm):
    def __init__(self, model: object = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model is not None:
            model_keys = set(model.__class__.__dict__.keys()) & \
                         model.__dict__['_sa_instance_state'].__dict__["expired_attributes"] & \
                         self.__dict__.keys()
            for i in model_keys:
                self.__dict__[i].data = getattr(model, i)
