import sqlalchemy
import os
from sqlalchemy.orm import declared_attr
from Project.settings import work_dir

from Project.data.db_session import SqlAlchemyBase
from Project.forms.Form import Form


class Block(SqlAlchemyBase):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))
    # sequence_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sequences.id'))

    def __init__(self, **kwargs):
        super().__init__()
        self.import_class_dict()

    def import_class_dict(self, **kwargs):
        if kwargs is not None:
            for i in kwargs:
                if i in self.__class__.__dict__.keys():
                    setattr(self, i, kwargs[i])
                else:
                    print(f'Error Key: {i} in class: {self.__class__.__name__}')

    def loading_data(self, request, **kwargs):
        self.import_class_dict()

    @staticmethod
    def getForm():
        return Form

    @staticmethod
    def label_block():
        return 'Блок'

    @declared_attr
    def article_id(self):
        return sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))

    @declared_attr
    def sequence_id(self):
        return sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sequences.id'))

    def get_html(self):
        path = os.path.join(work_dir, 'templates', 'Blocks')
        return open(os.path.join(path, f'{self.__class__.__name__}.html'), 'r',
                    encoding="UTF-8").read()


def check(obj):
    pathes = [
        os.path.join(work_dir, 'templates', 'Blocks'),
        os.path.join(work_dir, 'templates', 'Blocks', 'create')
    ]
    for path in pathes:
        if not os.path.isdir(path):
            os.makedirs(path)
        path_file = os.path.join(path, f'{obj.__name__}.html')
        if not os.path.isfile(path_file):
            open(path_file, 'w+', encoding="UTF-8").close()
