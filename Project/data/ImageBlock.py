import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class ImageBlock(SqlAlchemyBase, UserMixin):
    __tablename__ = 'image_blocks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))
    sequence = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('sequences.id'))