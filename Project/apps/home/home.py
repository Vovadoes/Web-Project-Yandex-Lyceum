from . import app_home

from flask import render_template
from Project.data.Article import Article
from Project.data.db_session import create_session


# @app_home.route("/")
# def home():
#     db_sess = create_session()
#     articles = db_sess.query(Article).all()
#     return render_template('home/home.html', articles=articles)


import flask
from flask import render_template, request
from .search import retrieve  #
from time import time
from . import app_home


@app_home.route("/", methods=['GET', "POST"])
def index():
    if flask.request.method == "POST":
        query = request.form.get("query")
        if query is not None:
            start_time = time()
            documents = retrieve(query)
            return render_template(
                'home/index.html',
                time="%.2f" % (time() - start_time),
                query=query,
                search_engine_name='Yandex',
                results=documents
            )
        else:
            return {}

    elif flask.request.method == "GET":  # основное окно
        start_time = time()
        query = ''
        documents = retrieve(query)
        return render_template(
            'home/index_2.html',
            time="%.2f" % (time() - start_time),
            query=query,
            search_engine_name='Yandex',
            results=documents
        )
