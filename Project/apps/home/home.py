from . import app_home

from flask import render_template
from Project.data.Article import Article
from Project.data.db_session import create_session, __factory


@app_home.route("/")
def home():
    db_sess = create_session()
    articles = db_sess.query(Article).all()
    return render_template('home/home.html', articles=articles)
