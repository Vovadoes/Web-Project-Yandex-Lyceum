from pprint import pprint

import flask
from flask import render_template, request
from .search import retrieve  #
from time import time
from . import app_home
from Project.forms.SortForm import SortForm
from Project.data.db_session import create_session
from Project.data.Article import Article
from Project.forms.SearchForm import SearchForm


@app_home.route("/", methods=['GET', "POST"])
def index():
    start_time = time()
    sort_form = SortForm()
    search_form = SearchForm()
    if flask.request.method == "POST":
        query = search_form.query.data
        print(f"{query=}")
        if query != '':
            documents = retrieve(query)
            # documents = [[heading, main_text, score, id]]
            dct = {i[3]: {"heading": i[0], "main_text": i[1], "score": i[2]} for i in documents}
            db_sess = create_session()
            articles = [db_sess.query(Article).filter(Article.id == i[3]).first() for i in documents]
        else:
            db_sess = create_session()
            articles = db_sess.query(Article).all()
            dct = {
                article.id: {
                    "heading": article.heading,
                    "main_text": article.get_MainIdeaBlock(db_sess).idea
                    if article.get_MainIdeaBlock(db_sess) is not None
                    else article.heading,
                    "score": 0
                } for article in articles
            }
        default_sort = search_form.search.data
        if sort_form.populated.data:
            articles.sort(key=lambda article: len(article.views))
        elif sort_form.time.data:
            articles.sort(key=lambda article: article.date_create, reverse=True)
        elif sort_form.time.data or default_sort:
            if query != '':
                articles.sort(key=lambda article: dct[article.id]["score"])
        dct_articles = {article: dct[article.id] for article in articles}
        pprint(dct_articles)
        return render_template(
            'home/index.html',
            time="%.2f" % (time() - start_time),
            query=query,
            search_engine_name='Yandex',
            sort_form=sort_form,
            dct_articles=dct_articles,
            search_form=search_form
        )

    elif flask.request.method == "GET":  # основное окно
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
            articles=articles,
            search_form=search_form,
            sort_form=sort_form
        )
