import json
import os

from flask import url_for
from werkzeug.utils import redirect

from . import app_articles
from Project.data.Article import Article
from Project.data.Sequence import Sequence
from Project.data.db_session import create_session
from Project.settings import work_dir
from Project.data.Blocks.MainIdeaBlock import MainIdeaBlock
from Project.data.Tag import Tag


# код для формирования базы данных
from Project.data.User import User


@app_articles.route("/resetting_my_database/")
def resetting_my_database():
    db_sess = create_session()
    path = os.path.join(work_dir, 'apps', 'articles', 'files')
    js2: dict = json.load(open(os.path.join(path, "js2.json"), encoding="UTF-8"))
    words: dict = json.load(open(os.path.join(path, "js.json"), encoding="UTF-8"))
    numbers: list[dict] = json.load(open(os.path.join(path, "numbers.json"), encoding="UTF-8"))
    js = {}
    for i in js2:
        js[int(i)] = js2[i]
    del js2
    tags = {}
    for i in words:
        tag = Tag()
        tag.name = i
        db_sess.add(tag)
        tags[tag.name] = tag
    db_sess.commit()
    db_sess.query()
    srt_idea_lst = []
    for dct in numbers:
        article = Article()
        article.heading = dct["title"]
        db_sess.add(article)
        main_idea_block = MainIdeaBlock()
        main_idea_block.idea = dct["history_text"]
        db_sess.add(main_idea_block)
        sequence = Sequence()
        db_sess.add(sequence)
        srt_idea_lst.append({"article_json_id": dct["id"], "MainIdeaBlock": main_idea_block,
                             "Sequence": sequence, "Article": article})
    db_sess.commit()
    # print(srt_idea_lst)
    user_id = db_sess.query(User).filter(User.email == "dereviannykh.v@gmail.com").first().id
    for dct in srt_idea_lst:
        article = dct["Article"]
        sequence = dct["Sequence"]
        main_idea_block = dct["MainIdeaBlock"]
        article_json_id = dct["article_json_id"]

        sequence.article_id = article.id
        sequence.number = 1

        main_idea_block.sequence_id = sequence.id
        main_idea_block.article_id = article.id

        article.MainIdeaBlockId = main_idea_block.id
        article.user_id = user_id
        # print(f"{article_json_id=}")
        # lst = [tags[name] for name in js[article_json_id]]
        # print(f"{lst=}")
        article.tags = article.tags + [tags[name] for name in js[article_json_id]]
    db_sess.commit()
    return redirect(url_for("start"))



"""
path = os.path.join(work_dir, 'apps', 'articles', 'files')
    js: dict = json.load(open(os.path.join(path, "js.json"), encoding="UTF-8"))
    numbers: list[dict] = json.load(open(os.path.join(path, "numbers.json"), encoding="UTF-8"))
    num = set()
    for i in js:
        num = num | set(js[i])
    dct = {i: set() for i in num}
    for i in js.keys():
        for j in js[i]:
            dct[j] = dct[j] | {i}
    for i in dct:
        dct[i] = list(dct[i])
    with open(os.path.join(path, "js2.json"), 'w+', encoding="UTF-8") as file:
        json.dump(dct, file, indent=2, ensure_ascii=False)
    return dct
"""
