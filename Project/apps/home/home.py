from datetime import datetime
from pprint import pprint

import flask
from flask import render_template, request
from .search import retrieve  #
from time import time
from . import app_home
from Project.forms.SortForm import SortForm
from Project.data.db_session import create_session
from Project.data.Article import Article


@app_home.route("/", methods=['GET', "POST"])
def index():
    sort_form = SortForm()
    if flask.request.method == "POST":
        query = request.form.get("query")
        if query is not None:
            start_time = time()
            documents = retrieve(query)
            # documents = [[heading, main_text, score, id]]
            db_sess = create_session()
            articles = [db_sess.query(Article).filter(Article.id == i[3]).first() for i in documents]
            print("articles")
            if sort_form.populated:
                print("123")
                # documents.sort(key=lambda obj: )
            elif sort_form.time:
                pass
            else:
                return render_template(
                    'home/index.html',
                    time="%.2f" % (time() - start_time),
                    query=query,
                    search_engine_name='Yandex',
                    results=documents,
                    sort_form=sort_form
                )
        else:
            return {}

    elif flask.request.method == "GET":  # основное окно
        start_time = time()
        db_sess = create_session()
        articles = sorted(
            db_sess.query(Article).all(),
            key=lambda article: article.date_create,
            reverse=True
        )
        return render_template(
            'home/index_2.html',
            time="%.2f" % (time() - start_time),
            search_engine_name='Yandex',
            articles=articles
        )
