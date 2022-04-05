import collections
import json
import os

import flask
from flask_login import current_user
from werkzeug.utils import redirect, secure_filename

from . import app_articles, ALLOWED_EXTENSIONS

from flask import render_template, request, url_for
from Project.data.Article import Article
from Project.data.Sequence import Sequence
from Project.data.db_session import create_session
from Project.data.Image import Image
from Project.settings import work_dir
from . import Blocks
from Project.fun import get_user
from Project.forms.ArticleForm import ArticleForm
from Project.data.Blocks.MainIdeaBlock import MainIdeaBlock
from Project.data.Tag import Tag
from Project.data.User import User


def set_sequence(article_id: int):
    db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    sequences: list[Sequence] = article.sequences
    sequences.sort(key=lambda x: x.number)
    for i in range(len(sequences)):
        sequences[i].number = i
    db_sess.commit()


@app_articles.route("/<int:article_id>/")
@get_user(required=False)
def article(user, article_id: int, *args, **kwargs):
    db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    if article is None:
        return {"res": "There is no article with this number"}
    set_sequence(article_id)
    blocks = []
    for Block in Blocks:
        blocks_block: Block = db_sess.query(Block).filter(Block.article_id == article_id)
        blocks += blocks_block
    sequences = []
    for block in blocks:
        sequence = db_sess.query(Sequence).filter(Sequence.id == block.sequence_id).first()
        if sequence not in article.sequences:
            db_sess.delete(sequence)
            raise ValueError(
                "Обнаружен блок не входящей в начальный класс Sequence.article_id."
                "Устранение: удаление связи Sequence и Blocks")
        sequences.append(sequence)
    db_sess.commit()
    blocks = sorted(blocks, key=lambda obj: sequences[blocks.index(obj)].number)
    author = db_sess.query(User).filter(User.id == article.user_id).first()
    return render_template("articles/article.html", blocks=blocks, article=article, author=author,
                           user=user)


@app_articles.route("/create/", methods=['GET', 'POST'])
@get_user(required=False)
def article_create(*args, **kwargs):
    if flask.request.method == "POST":
        form = ArticleForm()
        if form.validate_on_submit():
            db_sess = create_session()
            article = Article()
            # article.user_id = user.id
            article.heading = form.heading.data
            db_sess.add(article)
            db_sess.commit()
            return redirect(f"/article/{article.id}/")
        else:
            return {"result": "The form is not filled out correctly"}
    elif flask.request.method == "GET":
        article_form = ArticleForm()
        return render_template("articles/create/article.html", form=article_form)
    else:
        return {"result": "Invalid method", "method": flask.request.method}


@app_articles.route("/<int:article_id>/edit", methods=['GET', 'POST'])
@get_user(required=False)
def edit_article(user, *args, **kwargs):
    if flask.request.method == "POST":
        pass
    elif flask.request.method == "GET":
        article_form = ArticleForm()
        pass


@app_articles.route("/")
def test():
    return {"res": True}


# код для формирования базы данных
def reset_the_database():
    db_sess = create_session()
    path = os.path.join(work_dir, 'apps', 'articles', 'files')
    js2: dict = json.load(open(os.path.join(path, "js2.json"), encoding="UTF-8"))
    words: dict = json.load(open(os.path.join(path, "js.json"), encoding="UTF-8"))
    numbers: list[dict] = json.load(open(os.path.join(path, "numbers.json"), encoding="UTF-8"))
    js = {}
    for i in js2:
        js[int(i)] = js2[i]
    del js2
    tags = {}
    for i in words:
        tag = Tag()
        tag.name = i
        db_sess.add(tag)
        tags[tag.name] = tag
    db_sess.commit()
    db_sess.query()
    srt_idea_lst = []
    for dct in numbers:
        article = Article()
        article.heading = dct["title"]
        db_sess.add(article)
        main_idea_block = MainIdeaBlock()
        main_idea_block.idea = dct["history_text"]
        db_sess.add(main_idea_block)
        sequence = Sequence()
        db_sess.add(sequence)
        srt_idea_lst.append({"article_json_id": dct["id"], "MainIdeaBlock": main_idea_block,
                             "Sequence": sequence, "Article": article})
    db_sess.commit()
    # print(srt_idea_lst)
    for dct in srt_idea_lst:
        article = dct["Article"]
        sequence = dct["Sequence"]
        main_idea_block = dct["MainIdeaBlock"]
        article_json_id = dct["article_json_id"]

        sequence.article_id = article.id
        sequence.number = 1

        main_idea_block.sequence_id = sequence.id
        main_idea_block.article_id = article.id

        article.MainIdeaBlockId = main_idea_block.id
        # print(f"{article_json_id=}")
        # lst = [tags[name] for name in js[article_json_id]]
        # print(f"{lst=}")
        article.tags = article.tags + [tags[name] for name in js[article_json_id]]
    db_sess.commit()


"""
path = os.path.join(work_dir, 'apps', 'articles', 'files')
    js: dict = json.load(open(os.path.join(path, "js.json"), encoding="UTF-8"))
    numbers: list[dict] = json.load(open(os.path.join(path, "numbers.json"), encoding="UTF-8"))
    num = set()
    for i in js:
        num = num | set(js[i])
    dct = {i: set() for i in num}
    for i in js.keys():
        for j in js[i]:
            dct[j] = dct[j] | {i}
    for i in dct:
        dct[i] = list(dct[i])
    with open(os.path.join(path, "js2.json"), 'w+', encoding="UTF-8") as file:
        json.dump(dct, file, indent=2, ensure_ascii=False)
    return dct
"""


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
