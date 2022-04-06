import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

association_table_article_tag = sqlalchemy.Table('association_Tag_Article', SqlAlchemyBase.metadata,
                                                 sqlalchemy.Column('tag_id',
                                                                   sqlalchemy.ForeignKey('tags.id')),
                                                 sqlalchemy.Column('article_id',
                                                                   sqlalchemy.ForeignKey(
                                                                       'articles.id'))
                                                 )


class Tag(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    articles = relationship("Article", secondary=association_table_article_tag,
                            back_populates="tags")

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')

    def __str__(self):
        return f"<Project.data.Tag.Tag object, name = {self.name}>"

    def __repr__(self):
        return self.__str__()
