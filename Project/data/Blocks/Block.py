import sqlalchemy
import os
from sqlalchemy.orm import declared_attr
from Project.settings import work_dir

from Project.data.db_session import SqlAlchemyBase


class Block(SqlAlchemyBase):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    # article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))
    # sequence_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sequences.id'))

    @declared_attr
    def article_id(self):
        return sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))

    @declared_attr
    def sequence_id(self):
        return sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sequences.id'))

    def get_html(self):
        path = os.path.join(work_dir, 'templates', 'Blocks')
        return open(os.path.join(path, f'{self.__class__.__name__}.html'), 'w+', encoding="UTF-8")


def check(obj):
    path = os.path.join(work_dir, 'templates', 'Blocks')
    if not os.path.isdir(path):
        os.makedirs(path)
    if os.path.exists(path):
        open(os.path.join(path, f'{obj.__name__}.html'), 'w+', encoding="UTF-8").close()
