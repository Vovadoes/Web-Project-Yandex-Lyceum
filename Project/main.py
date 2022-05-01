import datetime
import os
import shutil

from flask import Flask
from flask import request, render_template
from flask_login import login_user, login_required, logout_user, LoginManager

from Project.CreateTags import create_tags
from Project.data.Article import Article
from Project.data.Blocks.TextBlock import TextBlock
from Project.data.Image import Image
from Project.data.Sequence import Sequence
from Project.data.Comment import Comment
from Project.forms.PasswordForm import PasswordForm
from apps.articles import app_articles
from apps.home import app_home
from apps.profile import app_profile
from apps.comments import app_comments
from apps.test import app_test
from forms.RegisterForm import RegisterForm
from forms.UserForm import LoginForm
from data import db_session
from Project.data.User import User

from werkzeug.utils import redirect

from Project.settings import work_dir, media_path, path_db, default_image, is_pycharm

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.register_blueprint(app_home, url_prefix='/home')
app.register_blueprint(app_profile, url_prefix='/profile')
app.register_blueprint(app_articles, url_prefix='/article')
app.register_blueprint(app_comments, url_prefix='/comment')
app.register_blueprint(app_test, url_prefix='/test')

login_manager = LoginManager()
login_manager.init_app(app)


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def start():
    # return redirect("/home/")
    return render_template("main.html")


# @app.route("/cookie_test")
# def cookie_test():
#     visits_count = int(request.cookies.get("visits_count", 0))
#     if visits_count:
#         res = make_response(
#             f"Вы пришли на эту страницу {visits_count + 1} раз")
#         res.set_cookie("visits_count", str(visits_count + 1),
#                        max_age=60 * 60 * 24 * 365 * 2)
#     else:
#         res = make_response(
#             "Вы пришли на эту страницу в первый раз за последние 2 года")
#         res.set_cookie("visits_count", '1',
#                        max_age=60 * 60 * 24 * 365 * 2)
#     return res
#
#
# @app.route("/session_test")
# def session_test():
#     visits_count = session.get('visits_count', 0)
#     session['visits_count'] = visits_count + 1
#     return make_response(
#         f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    password_form = PasswordForm()
    if request.method == "POST":
        if register_form.validate_on_submit() and password_form.validate_on_submit():
            if password_form.password.data != password_form.password_again.data:
                return render_template(
                    'register.html', title='Регистрация',
                    register_form=register_form,
                    password_form=password_form,
                    message="Пароли не совпадают"
                )
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == register_form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       register_form=register_form, password_form=password_form,
                                       message="Такой пользователь уже есть")
            user = User(
                email=register_form.email.data,
                name=register_form.name.data,
                age=register_form.age.data
            )
            user.set_password(password_form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
    else:
        return render_template(
            'register.html',
            title='Регистрация',
            register_form=register_form,
            password_form=password_form
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    register_form = LoginForm()
    password_form = PasswordForm()
    if register_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == register_form.email.data).first()
        if user and user.check_password(password_form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               register_form=register_form, password_form=password_form)
    return render_template('login.html', title='Авторизация',
                           register_form=register_form, password_form=password_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('Not_found.html')


db_session.global_init(path_db)
db_sess = db_session.create_session()
user = db_sess.query(User).filter(User.email == 'dereviannykh.v@gmail.com').first()
if user is None:
    user = User(
        email='dereviannykh.v@gmail.com',
        name='Vovik48rus',
        super_user=True,
    )
    user.set_password("Vovik48rus123")
    db_sess.add(user)
    db_sess.commit()
    img = Image()
    name = os.path.split(default_image)[1]
    path = img.generate_path(name, set_path=True)
    shutil.copyfile(os.path.join(work_dir, default_image),
                    os.path.join(os.path.join(work_dir, 'static', media_path), path))
    db_sess.add(img)
    db_sess.commit()
    article = Article(heading="Test 1 vovik", )
    article.user_id = user.id
    article.sources = "https://ru.wikipedia.org/wiki"
    article.image_id = img.id
    db_sess.add(article)
    db_sess.commit()
    sequence = Sequence()
    sequence.article_id = article.id
    sequence.number = 0
    db_sess.add(sequence)
    db_sess.commit()
    text_block = TextBlock()
    text_block.article_id = article.id
    text_block.text = "Text: vovik"
    text_block.heading = "Test1"
    text_block.sequence_id = sequence.id
    db_sess.add(text_block)
    db_sess.commit()
    comment = Comment()
    comment.text = 'Комментарий'
    comment.article = article
    comment.user = user
    db_sess.add(comment)
    db_sess.commit()
    create_tags(article.heading, article=article, db_sess=db_sess)

if is_pycharm:
    app.run(port=8080, host='localhost', debug=True)
