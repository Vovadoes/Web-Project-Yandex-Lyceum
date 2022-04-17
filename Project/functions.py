from sqlalchemy.orm import Session

from Project.CreateTags import create_tags
from Project.data.Article import Article
from Project.data.Blocks.MainIdeaBlock import MainIdeaBlock


def recreate_tags(article: Article, db_sess: Session = None, commit: bool = True):
    if commit:
        article.tags = []
        db_sess.commit()
    create_tags(article.heading, article, db_sess)
    if article.MainIdeaBlockId is not None:
        main_idea_block: MainIdeaBlock = db_sess.query(MainIdeaBlock).filter(
            MainIdeaBlock.id == article.MainIdeaBlockId).first()
        if main_idea_block is not None:
            create_tags(main_idea_block.idea, article, db_sess)
    if commit:
        db_sess.commit()
