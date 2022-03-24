import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

from .Tag import association_table


class Article(SqlAlchemyBase, UserMixin):
    __tablename__ = 'articles'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text_blocks = relationship("TextBlock")
    image_blocks = relationship("ImageBlock")
    tags = relationship("Tag", secondary=association_table, back_populates="articles")
    sources = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sequence = relationship("Sequence", back_populates="article_id")
