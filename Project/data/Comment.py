from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Session
from Project.data.db_session import create_session

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, UserMixin):
    __tablename__ = 'comment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    article_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('articles.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")
