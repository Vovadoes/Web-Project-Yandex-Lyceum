import os
import shutil
from pprint import pprint
from tempfile import NamedTemporaryFile

import sqlalchemy
from werkzeug.utils import secure_filename

from .db_session import SqlAlchemyBase
from Project.settings import work_dir, media_path, allowed_file, default_image


class Image(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, unique=True)

    def get_path(self):
        return os.path.join(media_path, self.path).replace('\\', '/')

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')

    @staticmethod
    def loading_from_request(request, default=True):
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    img = Image()
                    print(f'{filename=}')
                    path = img.generate_path(filename, set_path=True)
                    file.save(os.path.join(os.path.join(work_dir, 'static', media_path), path))
                    return img
        if default:
            img = Image()
            name = os.path.split(default_image)[1]
            path = img.generate_path(name, set_path=True)
            shutil.copyfile(os.path.join(work_dir, default_image),
                            os.path.join(os.path.join(work_dir, 'static', media_path), path))
            # path, name = os.path.split(default_image)
            # img.generate_path(name, set_path=True, path_dir=os.path.join(work_dir, path))
            return img

    @staticmethod
    def set_default():
        img = Image()
        name = os.path.split(default_image)[1]
        path = img.generate_path(name, set_path=True)
        shutil.copyfile(os.path.join(work_dir, default_image),
                        os.path.join(os.path.join(work_dir, 'static', media_path), path))
        # path, name = os.path.split(default_image)
        # img.generate_path(name, set_path=True, path_dir=os.path.join(work_dir, path))
        return img


    # def copy_image(self, image_path):
    #     path_dir = os.path.join(work_dir, 'media')
    #     with NamedTemporaryFile(dir=path_dir) as tf:
    #         filename, file_extension = os.path.splitext(image_path)
    #         name_new_file = tf.name
    #         with open(os.path.join(path_dir, name_new_file + file_extension), 'w+') as f2:
    #             with open(image_path, 'rb') as f1:
    #                 f2.write(f1.read())
    #                 self.path = os.path.join(name_new_file + file_extension)

    def generate_path(self, name, set_path=False, path_dir=None):
        if path_dir is None:
            path_dir = os.path.join(work_dir, 'static', media_path)
        filename, file_extension = os.path.splitext(name)
        tf = NamedTemporaryFile(dir=path_dir)
        name = os.path.basename(tf.name)
        if set_path:
            self.path = os.path.join(name + file_extension)
        return os.path.join(name + file_extension)

    def __repr__(self):
        return str(self.path)
