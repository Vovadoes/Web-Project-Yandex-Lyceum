import os
from tempfile import NamedTemporaryFile
from typing import Union, Any

import sqlalchemy
from .db_session import SqlAlchemyBase
from Project.settings import work_dir


class Image(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, unique=True)

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')

    # def copy_image(self, image_path):
    #     path_dir = os.path.join(work_dir, 'media')
    #     with NamedTemporaryFile(dir=path_dir) as tf:
    #         filename, file_extension = os.path.splitext(image_path)
    #         name_new_file = tf.name
    #         with open(os.path.join(path_dir, name_new_file + file_extension), 'w+') as f2:
    #             with open(image_path, 'rb') as f1:
    #                 f2.write(f1.read())
    #                 self.path = os.path.join(name_new_file + file_extension)

    def generate_path(self, name, set_path=False):
        path_dir = os.path.join(work_dir, 'media')
        filename, file_extension = os.path.splitext(name)
        tf = NamedTemporaryFile(dir=path_dir)
        name = os.path.basename(tf.name)
        if set_path:
            self.path = os.path.join(name + file_extension)
        return os.path.join(name + file_extension)

    def __repr__(self):
        return str(self.path)
