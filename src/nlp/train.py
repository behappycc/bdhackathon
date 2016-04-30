import sys 
sys.path.append("../")
from web_util import load_json, write_json
import os
import jieba
import jieba.posseg as pseg
jieba.load_userdict('dict.txt.big')
import re
#import extraDict
#import operator
from gensim import corpora, models, similarities  
import time
import datetime
import pymongo
from pymongo import MongoClient

def main():
    board = 'Japan_Travel'
    conn = MongoClient('localhost', 27017)
    db = conn['bdhackthon']
    collection = db[board]
    d_start = datetime.datetime(2016, 1, 1, 0)
    d_end = datetime.datetime(2016, 3, 1, 0)

    t_start = time.time()
    # bulil corpus
    if os.path.exists('corpus_data.json'):
        corpus_data = load_json('corpus_data.json')
    else:
        corpus_data = {}
    corpus = []
    articles = collection.find({
        "$or":[
        {"article_title": {"$regex": "\[[遊食]記\].*(東京)+.*"}, "date": {"$gt": d_start, "$lt": d_end}},
        {"article_title": {"$regex": "\[住宿\].*(東京)+.*"}, "date": {"$gt": d_start, "$lt": d_end}}]
    }, no_cursor_timeout=True).batch_size(20)
    print('Total:', articles.count())
    index_aid = {}  # map index of corpus to article_id
    i = 0
    tmp_data = {}
    for article in articles:
        #if i==80:
        #    break
        tmp_data[article['article_id']] = (article['article_title'], article['content'])
        index_aid[str(i)] = article['article_id']
        print(i)
        #print(article, article['article_title'])
        print(article['article_title'])
        #print(article['content'])
        #print(article)
        if article['article_id'] in corpus_data.keys():
            corpus.append(corpus_data[article['article_id']]['feature'])
            corpus_data[article['article_id']]['index'] = i
            i = i+1
            continue
        else:
            doc = []
            doc += splitWord(article['article_title'])
            doc += splitWord(article['content'])
            corpus_data[article['article_id']] = {
                'feature': doc,
                'topic': [],
                'index': i
            }
            corpus.append(doc)
            i = i+1
        #input()
    t_end = time.time()
    write_json(corpus_data, 'corpus_data.json')
    print('time elapsed for building corpus: %f minutes' % ((t_end-t_start)/60.0))

    dictionary = corpora.Dictionary(corpus)
    stoplist = [line.lower().split()[0] for line in open('stop_words.txt', 'r')]
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    #once_ids = []
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    #print(dictionary)
    #print(dictionary.dfs)
    #pprint(dictionary.token2id)
    dictionary.save('train.dict')  # store the dictionary, for future reference
    
    corpus_bow = [dictionary.doc2bow(doc) for doc in corpus]
    corpora.MmCorpus.serialize('train.mm', corpus_bow) # store to disk, for later use
    
    tfidf = models.TfidfModel(corpus_bow) # initialize (train) a model
    tfidf.save('train.tfidf')
    corpus_tfidf = tfidf[corpus_bow]
    
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, alpha='auto', num_topics=50)
    #print(lda.print_topics(50))
    lda.save('train.lda')
    corpus_lda = lda[corpus_tfidf]
    index = similarities.MatrixSimilarity(corpus_lda)  # transform corpus to LDA space and index it
    index.save('train.index')
    
    topic = {}
    for i in range(len(corpus_lda)):
        #print(corpus_lda[i])
        #print(corpus[i])
        key = max(corpus_lda[i], key=lambda x: abs(x[1]))[0]
        if key in topic.keys():
            topic[key].append(i)
        else:
            topic[key] = [i]
        #input()
    
    vec_topic = {}
    print('%d topics identified. Classify them:' % len(topic))

    old_corpus_data = load_json('old_model/corpus_data.json')
    for k, v in topic.items():
        print('Group %s (%d):' % (k, len(v)))
        for c_index in v:
            a_id = index_aid[str(c_index)]
            #if a_id in corpus_data.keys():
            if a_id in old_corpus_data.keys():
                #print(corpus_data[a_id]['topic'])
                if not old_corpus_data[a_id]['topic']:
                    #print(corpus_data[a_id]['feature'])
                    print(tmp_data[a_id])
                    line = input('Enter topics, separate by space: ')
                    corpus_data[a_id]['topic'] = line.split(' ')
                else:
                    corpus_data[a_id]['topic'] = old_corpus_data[a_id]['topic']
            else:
                raise ValueError('Empty article_id')
        write_json(corpus_data, 'corpus_data_labeled.json')

def splitWord(raw_str):
    doc = []
    #expr = re.compile(r'[^\u4e00-\u9fa5\s\w]')
    expr = re.compile(r'[^\u2E80-\u9FFF\s\w]')  # Chinese/Japanese/Korean
    for word, flag in pseg.cut(re.sub(expr, '', raw_str)):
        if(flag in ['n', 'nr', 'ns', 'nt', 'nz', 'v', 'a', 'd', 'eng']) and (len(word)>1):
            if word.lower() != 'fw':
                doc.append(word)
    return doc

if __name__ == '__main__':
    main()
