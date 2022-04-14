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


dler = nltk.downloader.Downloader()
nltk.download('stopwords')
sw_eng = set(stopwords.words('english'))
stemmer = SnowballStemmer(language='english')
dler.download('averaged_perceptron_tagger')
dler.download('wordnet')


def get_clean(x):
    x = str(x).lower().replace('\\', '').replace('_', ' ')
    x = re.sub("(.)\\1{2,}", "\\1", x)
    x = re.sub(r'[^\w\s]', '', x)
    return x


def get_wordnet_pos(treebank_tag):
    my_switch = {
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'N': wordnet.NOUN,
        'R': wordnet.ADV,
    }
    for key, item in my_switch.items():
        if treebank_tag.startswith(key):
            return item
    return wordnet.wordnet.NOUN


def my_lemmatizer(sent):
    lemmatizer = WordNetLemmatizer()
    tokenized_sent = sent.split()
    pos_tagged = [(word, get_wordnet_pos(tag))
                  for word, tag in pos_tag(tokenized_sent)]
    return ' '.join([lemmatizer.lemmatize(word, tag)
                     for word, tag in pos_tagged])


def preprocessing(s: str):
    s = get_clean(s)
    slave = []
    for word in s.split():
        if not word[0].isdigit():
            if not word in sw_eng:
                slave.append(word)
    s = ' '.join(slave)
    s = my_lemmatizer(s)
    return s


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
        result = db_sess.query(Tag).filter(Tag.name == i).first()
        if result is not None:
            id_word.append(result.id)
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