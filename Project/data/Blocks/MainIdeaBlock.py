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

    def loading_data(self, request, db_sess: Session, form, is_create=True, **kwargs):
        from Project.functions.articles.tags import recreate_tags
        super(MainIdeaBlock, self).loading_data(request, db_sess, form, **kwargs)
        article = db_sess.query(Article).filter(Article.id == self.article_id).first()
        if article.MainIdeaBlockId is None or not is_create:
            if not is_create:
                recreate_tags(article, db_sess)
            return True
        else:
            return abort(404)

    def change_db(self, db_sess: Session, result, *args, **kwargs):
        from Project.CreateTags import create_tags

        if result:
            article = db_sess.query(Article).filter(Article.id == self.article_id).first()
            article.MainIdeaBlockId = self.id
            db_sess.commit()
            create_tags(self.idea, article=article, db_sess=db_sess)

    def preparing_for_deletion(self, db_sess: Session, *args, **kwargs):
        super(MainIdeaBlock, self).preparing_for_deletion(db_sess, *args, **kwargs)
        article = db_sess.query(Article).filter(Article.MainIdeaBlockId == self.id).first()
        if article is not None:
            article.MainIdeaBlockId = None

    @staticmethod
    def getForm():
        return MainIdeaForm

    @staticmethod
    def label_block():
        return 'Блок с главной идеей'


Blocks_lst.append(MainIdeaBlock)
