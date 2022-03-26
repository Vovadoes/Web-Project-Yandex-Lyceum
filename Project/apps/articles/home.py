import os

from werkzeug.utils import redirect, secure_filename

from . import app_articles, ALLOWED_EXTENSIONS

from flask import render_template, request, url_for
from Project.data.Article import Article
from Project.data.Sequence import Sequence
from Project.data.db_session import create_session
from Project.data.Image import Image
from Project.settings import work_dir


def set_sequence(article_id: int):
    db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    sequences: list[Sequence] = article.sequences
    sequences.sort(key=lambda x: x.numder)
    for i in range(len(sequences)):
        sequences[i].numder = i
    db_sess.commit()


# @app_articles.route("/<int:article_id>")
# def article(article_id: int):
#     set_sequence(article_id)
#     db_sess = create_session()
#     article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
#     text_blocks = article.text_blocks
#     image_blocks = article.image_blocks
#     blocks: list = text_blocks + image_blocks
#     numders = []
#     for block in blocks:
#         sequence: Sequence = db_sess.query(Sequence).filter(
#             Sequence.id == block.sequence_id).first()
#         numders.append(sequence.numder)
#     sequence_blocks = sorted(blocks, key=lambda x: numders[blocks.index(x)])
#     print(sequence_blocks)
#     return render_template('home/home.html', sequence_blocks=sequence_blocks)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app_articles.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        db_sess = create_session()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img = Image()
            path = img.generate_path(filename, set_path=True)
            file.save(os.path.join(os.path.join(work_dir, 'media'), path))
            db_sess.add(img)
            db_sess.commit()
            return redirect(url_for('app_articles.upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form'''
