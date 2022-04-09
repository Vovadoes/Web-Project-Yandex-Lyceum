from Project.apps.home.dop_func import preprocessing, find_id_articles


def retrieve(query):  # принимает строку из поиска

    # возвращает начальный список релевантных документов
    # (желательно, не бесконечный)
    # возравщает список документов
    query = preprocessing(query).split()  # нормализация текста
    all_doc = find_id_articles(query)
    if len(all_doc) == 0:
        all_doc = [['Нечего не найденно', 'nothing', 0, 0]]
    return all_doc
