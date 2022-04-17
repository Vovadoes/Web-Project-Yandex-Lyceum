from Project.apps.home.preprocessing import preprocessing
from Project.data.Article import Article
from sqlalchemy.orm import Session

from Project.data.Tag import Tag


def create_tags(string: str, article: Article, db_sess: Session = None, commit: bool = True):
    words = preprocessing(string).split()
    tags = set([tag.name for tag in article.tags])
    for word in words:
        tag = db_sess.query(Tag).filter(Tag.name == word).first()
        if tag is None:
            tag = Tag(name=word)
        if word not in tags:
            tag.articles.append(article)
            tags.add(word)
    if commit:
        db_sess.commit()
