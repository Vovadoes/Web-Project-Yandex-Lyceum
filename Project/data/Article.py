from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Session
from Project.data.db_session import create_session
from Project.data.Image import Image

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
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'),
                                 nullable=True)

    views = relationship("User", secondary=association_table_views, back_populates="views")
    user = relationship("User", back_populates="article")
    tags = relationship("Tag", secondary=association_table_article_tag, back_populates="articles")
    sources = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sequences = relationship("Sequence", backref="articles")
    comments = relationship("Comment", back_populates="article")

    def get_MainIdeaBlock(self, db_sess: Session = None):
        from Project.data.Blocks.MainIdeaBlock import MainIdeaBlock
        if db_sess is None:
            db_sess = create_session()
        if self.MainIdeaBlockId is not None:
            main_idea_block = db_sess.query(MainIdeaBlock).filter(
                MainIdeaBlock.id == self.MainIdeaBlockId).first()
            return main_idea_block

    def get_image(self, db_sess: Session = None):
        if db_sess is None:
            db_sess = create_session()
        if self.image_id is not None:
            print(self.image_id)
            img = db_sess.query(Image).filter(Image.id == self.image_id).first()
            return img

    def __init__(self, **kwargs):
        super().__init__()
        for i in kwargs:
            if i in self.__class__.__dict__.keys():
                setattr(self, i, kwargs[i])
            else:
                print(f'Error Key: {i} in class: {self.__class__.__name__}')
