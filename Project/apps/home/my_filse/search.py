import random
import pandas as pd
import joblib
import pickle
from dop_func import preprocessing, find_id_articles


class Document:
    def __init__(self, title, text):
        # можете здесь какие-нибудь свои поля подобавлять
        self.title = title
        self.text = text

    def format(self, query):
        # возвращает пару тайтл-текст, отформатированную под запрос
        return [self.title, self.text + ' ...']  # сдесь монжо изменить размер текста


# index = []
# vectorizer_1 = joblib.load('vectroizer_1.pkl')
# vectorizer_2 = joblib.load('vectroizer_2.pkl')
# with open('id_title.pickle', 'rb') as fp:
#     id_title = pickle.load(fp)
# with open('id_content.pickle', 'rb') as fp:
#     id_content = pickle.load(fp)
# df_pr1 = pd.read_csv('dataframe_super.csv')
# df_pr2 = pd.read_csv('dataframe_2.csv')

def score(query, document):  # принимает строку и документ
    # возвращает какой-то скор для пары запрос-документ
    # больше -- релевантнее
    return random.random()


def retrieve(query):  # принимает строку из поиска

    # возвращает начальный список релевантных документов
    # (желательно, не бесконечный)
    # возравщает список документов
    query = preprocessing(query).split()  # нормализация текста
    all_doc = find_id_articles(query)
    if len(all_doc) == 0:
        all_doc = [['Нечего не найденно', 'nothing', 0, 0]]
    return all_doc
    # candidates = set()  # множество наших индексов
    # for doc in query:
    #     candidates.add(id_title[doc])
    #     candidates.add(id_content[doc])
    # if len(candidates) == 0:
    #     return [index[0], index[1]]  # Изменено
    # res = []
    # for i in list(candidates):
    #     res.append(index[i])
    # return res
