from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

from .Tag import association_table_article_tag

association_table_views = sqlalchemy.Table(
    'association_table_views', SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('user.id')),
    sqlalchemy.Column('article_id', sqlalchemy.ForeignKey('articles.id'))
)


class Article(SqlAlchemyBase, UserMixin):
    __tablename__ = 'articles'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    heading = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    MainIdeaBlockId = sqlalchemy.Column(sqlalchemy.Integer,
                                        sqlalchemy.ForeignKey('MainIdea_Block.id'))

    views = relationship("User", secondary=association_table_views, back_populates="views")
    user = relationship("User", back_populates="article")
    tags = relationship("Tag", secondary=association_table_article_tag, back_populates="articles")
    sources = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sequences = relationship("Sequence", backref="articles")

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')
