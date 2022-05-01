from pprint import pprint

from flask_wtf import FlaskForm

from Project.settings import replace_the_mat_with

from Project.apps.home.delete_swear import RegexpProc


class Base:
    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')

    def import_class_form(self, form: FlaskForm = None, *args, **kwargs):
        if form is not None:
            dct = form.__dict__
            st = set(dct.keys()) & set(self.__dict__.keys())
            for i in st:
                setattr(self, i, RegexpProc.replace(dct[i].data, repl=replace_the_mat_with))

    def import_class_dict(self, dct: dict = None, *args, **kwargs):
        if dct is not None:
            for i in dct:
                if i in self.__class__.__dict__.keys():
                    setattr(self, i, RegexpProc.replace(dct[i].data, repl=replace_the_mat_with))
