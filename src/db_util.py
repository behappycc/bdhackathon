from operator import itemgetter

# mongodb module
from pymongo import MongoClient

DB_IP = "localhost"  # use local DB
DB_PORT = 27017  # default MongoDB port
DB_NAME = 'bdhackathon'  # use the collection


def search_db(collection, query):
    # input query would be split by space
    # output result is done by AND logic
    item_list = []
    query_list = query.split(' ')
    # cursor = collection.find({"keywords": {'$all': query_list}})
    # print cursor.count()

    cursor_list = []
    cursor_count_list = []
    for q in query_list:
        cursor = collection.find({"$or": [
            {"content": {'$regex': '(' + q + ')'}},
            {"article_title": {'$regex': '(' + q + ')'}}
        ]})
        if cursor.count() == 0:
            continue
        # print query
        cursor_list.append(cursor)
        cursor_count_list.append(cursor.count())
        # print cursor.count()

    if len(cursor_list) == 0:
        return []

    min_cursor = cursor_list[min(enumerate(cursor_count_list), key=itemgetter(1))[0]]

    for item in min_cursor:
        ss = item['article_title'] + ' ' + item['content']
        is_contained = True
        for q in query_list:
            try:
                ss.index(q)
            except ValueError:
                is_contained = False
                break
        if is_contained:
            item_list.append(item)

    return item_list


def test_search():
    client = MongoClient(DB_IP, DB_PORT)
    collection = client[DB_NAME]['Japan_Travel']

    result_list = search_db(collection, '東京 必買 伴手禮')
    print('found: ' + str(len(result_list)))
    for s in result_list[0: min(10, len(result_list))]:
        print(s)


if __name__ == '__main__':
    test_search()
