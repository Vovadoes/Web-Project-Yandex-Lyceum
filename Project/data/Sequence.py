import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Sequence(SqlAlchemyBase, UserMixin):
    __tablename__ = 'sequences'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))

    number = sqlalchemy.Column(sqlalchemy.Integer)
