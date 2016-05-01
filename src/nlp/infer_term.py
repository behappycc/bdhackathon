import sys
sys.path.append("../")
from web_util import load_json, write_json
from db_util import search_db
from location_converter import translate_location
import pymongo
from pymongo import MongoClient

def infer(collection, term):
    print('Query term:', term)

    result_list = search_db(collection, term)
    popularity = len(result_list)
    if popularity == 0:
        return [], popularity, '', {}, {}, []
    print('Found articles (popularity): ' + str(popularity))
    
    atopic = load_json('article_topic.json')
    topic_count = {}
    topic_article = {}
    total = 0
    for s in result_list:
        a_id = s['article_id']
        a_date = s['date']
        if a_id in atopic.keys():
            #print(atopic[s['article_id']])
            for t in atopic[a_id]:
                total += 1
                if t in topic_count.keys():
                    topic_count[t] += 1
                else:
                    topic_count[t] = 1
                if t in topic_article.keys():
                    if (a_id, len(atopic[a_id])) not in topic_article[t]:
                        topic_article[t].append((a_id, len(atopic[a_id]), a_date))
                else:
                    topic_article[t] = [(a_id, len(atopic[a_id]), a_date)]
    
    #print(topic_article)
    for k, v in topic_article.items():
        topic_article[k] = sorted(v, key=lambda x:(x[1], -(x[2].toordinal())))
    #print(topic_article)
    article = {}
    for k, v in topic_article.items():
        article[k] = [ele[0] for ele in v]
    #print(article)

    topic_list = []
    for k, v in topic_count.items():
        topic_list.append((k, v, round(v/float(total), 4)))
    topic_list = sorted(topic_list, key=lambda x:x[1], reverse=True)

    ref = []
    for _t in topic_list:
        ref += article[_t[0]]
        if len(ref)>2:
            break
    ref = ref[:3]

    coord = translate_location(term)

    url = 'https://www.ptt.cc/bbs/Japan_Travel/'
    return topic_list, popularity, url, article, ref, coord


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    collection = client['bdhackthon']['Japan_Travel']
    
    new_term_data = {}
    term_data = load_json('term.json')
    for term in term_data.keys():
        tlist, popularity, url, article, ref, coord = infer(collection, term)
        new_term_data[term] = {
            'topic': tlist,
            'popularity': popularity,
            'url': url,
            'article': article,
            'ref': ref,
            'coord': coord
        }
        write_json(new_term_data, 'new_term.json')
        category = load_json('category.json')
        for t in tlist:
            print(category[t[0]], t[1], t[2])
        print('url:', url)
        for k, v in article.items():
            print(category[k], v)
        print('ref:', ref)
        print('coord:', coord)
    #term = '赤城神社'
    #term = '格拉斯麗'
    #tlist, popularity, url, article, ref, coord = infer(collection, term)
