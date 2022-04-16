from pprint import pprint

import sqlalchemy
import os
from sqlalchemy.orm import declared_attr

from Project.data.Sequence import Sequence
from Project.settings import work_dir

from Project.data.db_session import SqlAlchemyBase, create_session
from Project.forms.Form import Form


class Block(SqlAlchemyBase):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))
    # sequence_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sequences.id'))

    def __init__(self, **kwargs):
        super().__init__()
        self.import_class_dict()

    def import_class_dict(self, dct: dict = None, *args, **kwargs):
        if dct is not None:
            for i in dct:
                if i in self.__class__.__dict__.keys():
                    setattr(self, i, dct[i].data)
                else:
                    print(f'Error Key: {i} in class: {self.__class__.__name__}')

    def loading_data(self, request, db_sess, form, **kwargs):
        self.import_class_dict(dct=form.__dict__)

    def change_db(self, db_sess, result, *args, **kwargs):
        pass

    def get_sequence(self, db_sess=None):
        if db_sess is None:
            db_sess = create_session()
        try:
            sequence = db_sess.query(Sequence).filter(Sequence.id == self.sequence_id).first()
            return sequence
        except Exception as error:
            pprint(error)
            return None

    @staticmethod
    def getForm():
        return Form

    @staticmethod
    def label_block():
        return 'Блок'

    def preparing_for_deletion(self, db_sess, *args, **kwargs):
        pass

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
