from pprint import pprint

from werkzeug.utils import redirect

from . import app_profile
from Project.functions.profile.profile import get_user
from flask import render_template, request, url_for

from Project.data.db_session import create_session
from Project.data.Article import Article
from Project.data.User import User
from Project.forms.PasswordForm import PasswordForm
from Project.forms.RegisterForm import RegisterForm


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
    form = RegisterForm()
    message = ''
    if request.method == "POST":
        if form.validate_on_submit():
            user.import_class_form(form)
            db_sess.commit()
            return redirect(url_for("app_profile.main"))
        else:
            message = "Форма не заполнена или отсутствует CSRF токен."
    elif request.method == "GET":
        return render_template("Profile/EditProfile.html", user=user, form=form)
    return render_template("Profile/EditProfile.html", user=user, form=form, message=message)


@app_profile.route("/replace_password", methods=["GET", "POST"])
@get_user()
def replace_password(user, *args, **kwargs):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user.id).first()
    form = PasswordForm()
    message = ""
    if request.method == "POST":
        if form.validate_on_submit():
            if form.password.data == form.password_again.data:
                user.set_password(form.password.data)
                db_sess.commit()
                return redirect(url_for("app_profile.main"))
            else:
                message = "Пароли не совпадают"
        else:
            message = "Форма не заполнена или отсутствует CSRF токен."
    elif request.method == "GET":
        return render_template("Profile/ReplacePassword.html", user=user, form=form)
    return render_template("Profile/ReplacePassword.html", user=user, form=form, message=message)
