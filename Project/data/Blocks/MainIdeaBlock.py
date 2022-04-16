import sqlalchemy
from sqlalchemy.orm import Session
from werkzeug.exceptions import abort

from .Block import Block
from .settings import Blocks_lst
from Project.forms.Blocks.MainIdeaForm import MainIdeaForm
from Project.data.Article import Article


class MainIdeaBlock(Block):
    __tablename__ = 'MainIdea_Block'
    __table_args__ = {'extend_existing': True}

    idea = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def loading_data(self, request, db_sess: Session, form, **kwargs):
        super(MainIdeaBlock, self).loading_data(request, db_sess, form, **kwargs)
        article = db_sess.query(Article).filter(Article.id == self.article_id).first()
        if article.MainIdeaBlockId is None:
            return True
        else:
            return abort(404)

    def change_db(self, db_sess: Session, result, *args, **kwargs):
        if result:
            article = db_sess.query(Article).filter(Article.id == self.article_id).first()
            article.MainIdeaBlockId = self.id
            db_sess.commit()


    @staticmethod
    def getForm():
        return MainIdeaForm

    @staticmethod
    def label_block():
        return 'Блок с главной идеей'


Blocks_lst.append(MainIdeaBlock)
