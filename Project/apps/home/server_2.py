import flask
from flask import Flask, render_template, request
from Project.apps.home.search import retrieve  #
from time import time

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET', "POST"])
def index():
    if flask.request.method == "POST":
        print(request.args)
        query = request.form.get("query")
        print(f"{query=}")
        if query is not None:
            start_time = time()
            documents = retrieve(query)
            return render_template(
                'index.html',
                time="%.2f" % (time() - start_time),
                query=query,
                search_engine_name='Yandex',
                results=documents
            )
        else:
            return {'123': query}

    elif flask.request.method == "GET":  # основное окно
        start_time = time()
        query = ''
        documents = retrieve(query)
        # documents = sorted(documents, key=lambda doc: -score(query, doc))
        # results = [doc.format(query) + ['%.2f' % score(query, doc)] for doc in documents]
        return render_template(
            'index_2.html',
            time="%.2f" % (time() - start_time),
            query=query,
            search_engine_name='Yandex',
            results=documents
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

# прикрепить id для ссылки
