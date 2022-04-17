import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from nltk import WordNetLemmatizer, pos_tag
from Project.data.db_session import create_session
from Project.data.Tag import Tag
from . import path_db
import os

from Project.data.Article import Article
from Project.data.Blocks.MainIdeaBlock import MainIdeaBlock


def find_id_articles(s: list, k=100):
    # Импорт библиотеки
    import sqlite3
    # os.path.join(os.getcwd(), 'Project', 'db', 'db.db')
    # Подключение к БД
    #  con = sqlite3.connect(path_db_danila)

    # Создание курсора
    #  cur = con.cursor()

    # s = ['accuracy', 'ace']
    # Выполнение запроса и получение всех результатов
    id_word = []
    id_articls = []
    db_sess = create_session()
    for i in s:
        print("-----------------------", f'{s=}')
        # result = cur.execute("""SELECT id FROM tags
        #         WHERE name like ?""", (i,)).fetchall()
        result = db_sess.query(Tag).filter(Tag.name == i).first().id
        if result is not None:
            id_word.append(result)
    for i in id_word:
        # result = cur.execute("""SELECT article_id FROM association_Tag_Article
        #                 WHERE tag_id = ?""", (i,)).fetchall()
        result = [j.id for j in db_sess.query(Tag).filter(Tag.id == i).first().articles]
        id_articls += result
    set_articls = set(id_articls)
    all_articls = sorted([[i, id_articls.count(i)] for i in set_articls], key=lambda x: x[1],
                         reverse=True)
    if len(all_articls) >= k + 1:
        all_articls = all_articls[:k]
    end_work = []
    for i in all_articls:
        id = i[0]
        score = i[1]
        article = db_sess.query(Article).filter(Article.id == id).first()
        heading, id_text = article.heading, article.MainIdeaBlockId
        main_text = db_sess.query(MainIdeaBlock).filter(MainIdeaBlock.id == id_text).first().idea
        # main_text = cur.execute("""SELECT idea FROM MainIdea_Block
        #                 WHERE id = ?""", (id_text,)).fetchall()[0][0]
        if len(heading) > 40:
            heading = heading[:40] + '...'
        if len(main_text) > 60:
            main_text = main_text[:60] + '...'
        end_work.append([heading, main_text, score, id])
    # con.close()
    return end_work
