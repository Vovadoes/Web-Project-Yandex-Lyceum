from pprint import pprint

from flask import render_template, request, url_for
from werkzeug.utils import redirect

from . import app_comments
from Project.apps.home.delete_swear import RegexpProc
from Project.data.db_session import create_session
from Project.functions.profile.profile import get_user
from Project.functions.articles.articles import get_article_id
from Project.data.Article import Article
from Project.data.Comment import Comment
from Project.forms.CommentForm import CommentForm
from Project.settings import replace_the_mat_with
from Project.data.User import User


@app_comments.route("/article/<int:article_id>/", methods=['GET'])
@get_article_id()
@get_user()
def view_comments(article_id: int, user: User, *args, **kwargs):
    db_sess = create_session()
    article = db_sess.query(Article).filter(Article.id == article_id).first()
    user = db_sess.query(User).filter(User.id == user.id).first()
    comments: list[Comment] = article.comments
    pprint(comments)
    return render_template("Comments/View.html", article=article, comments=comments, user=user)


@app_comments.route("/article/<int:article_id>/create", methods=['GET', 'POST'])
@get_article_id()
@get_user()
def create_comments(article_id: int, user: User, *args, **kwargs):
    db_sess = create_session()
    article = db_sess.query(Article).filter(Article.id == article_id).first()
    user = db_sess.query(User).filter(User.id == user.id).first()
    form = CommentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            comment = Comment()
            comment.text = RegexpProc.replace(form.text.data, repl=replace_the_mat_with)
            comment.article = article
            comment.user = user
            db_sess.add(comment)
            db_sess.commit()
            return redirect(url_for("app_comments.view_comments", article_id=article_id))
        else:
            return {}
    elif request.method == "GET":
        return render_template("Comments/CreateComment.html", article=article, form=form, user=user)
