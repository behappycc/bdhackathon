import sys
sys.path.append("../")
from web_util import load_json, write_json
from db_util import search_db
import pymongo
from pymongo import MongoClient

def infer(collection, term):
    print('Query term:', term)

    result_list = search_db(collection, term)
    print('Found articles: ' + str(len(result_list)))
    
    atopic = load_json('article_topic.json')
    topic = {}
    total = 0
    for s in result_list:
        if s['article_id'] in atopic.keys():
            #print(atopic[s['article_id']])
            for t in atopic[s['article_id']]:
                total += 1
                if t in topic.keys():
                    topic[t] += 1
                else:
                    topic[t] = 1

    topic_list = []
    for k, v in topic.items():
        topic_list.append((k, v, v/float(total)))
    topic_list = sorted(topic_list, key=lambda x:x[1], reverse=True)
    return(topic_list)


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    collection = client['bdhackthon']['Japan_Travel']
    #term = '赤城神社'
    term = '格拉斯麗'
    tlist = infer(collection, term)
    category = load_json('category.json')
    for t in tlist:
        print(category[t[0]], t[1], t[2])

