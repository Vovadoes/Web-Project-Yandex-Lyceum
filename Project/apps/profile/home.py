from . import app_profile
from Project.functions.profile.profile import get_user
from flask import render_template, request

from Project.data.db_session import create_session
from Project.data.Article import Article
from Project.data.User import User


@app_profile.route("/")
@get_user(required=False)
def main(user: User, *args, **kwargs):
    return render_template('Profile/Main.html', user=user)
    pass


@app_profile.route("/articles")
@get_user(required=True)
def articles(user: User, *args, **kwargs):
    db_sess = create_session()
    articles = db_sess.query(Article).filter(Article.user_id == user.id)
    return render_template("Profile/Articles.html", articles=articles)


@app_profile.route("/comments")
@get_user()
def comments(user: User, *args, **kwargs):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user.id).first()
    comments = user.comments
    return render_template("Profile/Comments.html", comments=comments)


@app_profile.route("/edit", methods=["GET", "POST"])
@get_user()
def edit(user, *args, **kwargs):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user.id).first()
    if request.method == "POST":
        pass
    elif request.method == "GET":
        pass
