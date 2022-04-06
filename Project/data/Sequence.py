import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Sequence(SqlAlchemyBase, UserMixin):
    __tablename__ = 'sequences'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))

    number = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')
