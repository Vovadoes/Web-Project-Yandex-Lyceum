from Project.apps.home.dop_func import find_id_articles
from .preprocessing import preprocessing


def retrieve(query):  # принимает строку из поиска

    # возвращает начальный список релевантных документов
    # (желательно, не бесконечный)
    # возравщает список документов
    query = preprocessing(query).split()  # нормализация текста
    all_doc = find_id_articles(query)
    return all_doc
