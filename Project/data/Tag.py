import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('association_Tag_Article', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('tag_id', sqlalchemy.ForeignKey('tags.id')),
                                     sqlalchemy.Column('article_id',
                                                       sqlalchemy.ForeignKey('articles.id'))
                                     )


class Tag(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    articles = relationship("Article", secondary=association_table, back_populates="tags")
