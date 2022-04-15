import werkzeug
from loguru import logger

from requests import Session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from . import app_articles

from flask import render_template, request
from Project.data.Article import Article
from Project.data.Sequence import Sequence
from Project.data.db_session import create_session
from . import Blocks
from Project.fun import get_user, user_is_author, get_article_id
from Project.forms.ArticleForm import ArticleForm
from Project.data.User import User


@logger.catch
def set_sequence(article_id: int, db_sess: Session = None):
    if db_sess is None:
        db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    sequences: list[Sequence] = article.sequences
    sequences.sort(key=lambda x: x.number)
    for i in range(len(sequences)):
        sequences[i].number = i
    db_sess.commit()


@logger.catch
def get_sort_blocks(article: Article, db_sess: Session = None):
    if db_sess is None:
        db_sess = create_session()
    blocks = []
    for Block in Blocks:
        blocks_block: Block = db_sess.query(Block).filter(Block.article_id == article.id)
        blocks += blocks_block
    sequences = []
    for block in blocks:
        sequence = db_sess.query(Sequence).filter(Sequence.id == block.sequence_id).first()
        if sequence not in article.sequences:
            db_sess.delete(sequence)
            logger.error("Обнаружен блок не входящей в начальный класс Sequence.article_id."
                         "Устранение: удаление связи Sequence и Blocks")
            raise ValueError(
                "Обнаружен блок не входящей в начальный класс Sequence.article_id."
                "Устранение: удаление связи Sequence и Blocks")
        sequences.append(sequence)
    db_sess.commit()
    blocks = sorted(blocks, key=lambda obj: sequences[blocks.index(obj)].number)
    return blocks


@app_articles.route("/<int:article_id>/")
@get_article_id()  # проверка статьи на существование
@get_user(required=False)
def article(user, article_id: int, *args, **kwargs):
    res = set_sequence(article_id)
    if res is not None:
        return res
    del res
    db_sess = create_session()
    article: Article = db_sess.query(Article).filter(Article.id == article_id).first()
    if article is None:
        return {"res": "There is no article with this number"}
    blocks = get_sort_blocks(article, db_sess)
    if user is not None:
        user = db_sess.query(User).filter(User.id == user.id).first()
        if article.id not in user.views:
            user.views.append(article)
            article.views.append(user)
            db_sess.commit()
    author = db_sess.query(User).filter(User.id == article.user_id).first()
    return render_template("articles/article.html", blocks=blocks, article=article, author=author,
                           user=user)


@app_articles.route("/create/", methods=['GET', 'POST'])
@get_user(required=False)
def article_create(user, *args, **kwargs):
    if request.method == "POST":
        form = ArticleForm()
        if form.validate_on_submit():
            db_sess = create_session()
            article = Article()
            article.user_id = user.id
            article.heading = form.heading.data
            db_sess.add(article)
            db_sess.commit()
            return redirect(f"/article/{article.id}/")
        else:
            return {"result": "The form is not filled out correctly"}
    elif request.method == "GET":
        article_form = ArticleForm()
        return render_template("articles/create/article.html", form=article_form)
    else:
        return {"result": "Invalid method", "method": request.method}


@app_articles.route("/<int:article_id>/edit", methods=['GET', 'POST'])
@get_article_id()  # проверка статьи на существование
@get_user(required=True)
@user_is_author(required=False)  # Пока выключим проверку
def edit_article(user: User, article_id: int, *args, **kwargs):
    if request.method == "POST":
        article_form = ArticleForm()
        if article_form.validate_on_submit():
            db_sess = create_session()
            article = db_sess.query(Article).filter(Article.id == article_id).first()
            article.heading = article_form.heading.data
            db_sess.commit()
            return redirect(f"/article/{article.id}/")
    elif request.method == "GET":
        db_sess = create_session()
        set_sequence(article_id, db_sess)
        article = db_sess.query(Article).filter(Article.id == article_id).first()
        blocks = get_sort_blocks(article, db_sess)
        article_form = ArticleForm(article)
        print(article.heading, article_form.heading.data)
        return render_template("articles/edit/article.html", form=article_form, article=article,
                               blocks=blocks)
    else:
        return abort(404)


@app_articles.route("/<int:article_id>/edit/add/block/place/<int:number>", methods=['GET'])
@get_article_id()
@get_user(required=True)
@user_is_author(required=False)  # Пока выключим проверку
def choosing_create_block(user: User, article_id: int, number: int, *args, **kwargs):
    db_sess = create_session()
    article = db_sess.query(Article).filter(Article.id == article_id).first()
    return render_template("articles/create/Choose_block.html", user=user, article=article,
                           number=number, Blocks=Blocks)


@app_articles.route("/<int:article_id>/edit/add/block/place/<int:number>/block/<int:number_block>",
                    methods=['GET', 'POST'])
@get_article_id()
@get_user(required=True)
@user_is_author(required=False)  # Пока выключим проверку
def create_block(user: User, article_id: int, number: int, number_block: int, *args, **kwargs):
    if not (0 <= number_block < len(Blocks)) or len(str(number_block)) > 1000000000:
        return abort(404)
    if len(str(number)) > 1000000000:
        return abort(404)
    if request.method == "POST":
        form = Blocks[number_block].getForm()()
        if form.validate_on_submit():
            db_sess = create_session()
            set_sequence(article_id, db_sess)
            article = db_sess.query(Article).filter(Article.id == article_id).first()
            blocks = get_sort_blocks(article, db_sess)
            for i in range(number, len(blocks)):
                sequence = db_sess.query(Sequence).filter(
                    Sequence.id == blocks[i].sequence_id).first()
                sequence.number += 1
            sequence = Sequence()
            sequence.article_id = article.id
            sequence.number = number
            db_sess.add(sequence)
            db_sess.commit()
            block = Blocks[number_block]()
            block.sequence_id = sequence.id
            block.article_id = article.id
            try:
                result = block.loading_data(request=request, db_sess=db_sess, form=form)
            except werkzeug.exceptions.NotFound:
                db_sess.delete(sequence)
                db_sess.commit()
                return abort(404)
            db_sess.add(block)
            db_sess.commit()
            result = block.change_db(db_sess=db_sess, result=result)
            if result is not None:
                return result
            return redirect(f"/article/{article.id}/")
    elif request.method == "GET":
        if 0 <= number_block < len(Blocks):
            form = Blocks[number_block].getForm()()
            return render_template(f"Blocks/create/{Blocks[number_block].__name__}.html", form=form)
        else:
            return abort(404)
    else:
        return {"res": True}
