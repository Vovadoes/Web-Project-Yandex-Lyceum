from . import app_articles

from flask import render_template
from Project.data.Article import Article
from Project.data.Sequence import Sequence
from Project.data.db_session import create_session


def set_sequence(article_id: int):
    db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    sequences: list[Sequence] = article.sequences
    sequences.sort(key=lambda x: x.numder)
    for i in range(len(sequences)):
        sequences[i].numder = i
    db_sess.commit()


@app_articles.route("/<int:article_id>")
def article(article_id: int):
    set_sequence(article_id)
    db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    text_blocks = article.text_blocks
    image_blocks = article.image_blocks
    blocks: list = text_blocks + image_blocks
    numders = []
    for block in blocks:
        sequence: Sequence = db_sess.query(Sequence).filter(Sequence.id == block.sequence_id).first()
        numders.append(sequence.numder)
    sequence_blocks = sorted(blocks, key=lambda x: numders[blocks.index(x)])
    print(sequence_blocks)
    return render_template('home/home.html', sequence_blocks=sequence_blocks)
