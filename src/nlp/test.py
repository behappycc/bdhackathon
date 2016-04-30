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
    # bulil testing corpus
    if os.path.exists('testing_corpus_data.json'):
        testing_corpus_data = load_json('testing_corpus_data.json')
    else:
        testing_corpus_data = {}
    testing_corpus = []
    articles = collection.find({
        "$or":[ 
        {"article_title": {"$regex": "\[[遊食]記\].*(東京)+.*"}, "date": {"$lt": d_start}},
        {"article_title": {"$regex": "\[住宿\].*(東京)+.*"}, "date": {"$lt": d_start}},
        {"article_title": {"$regex": "\[[遊食]記\].*(東京)+.*"}, "date": {"$gt": d_end}},
        {"article_title": {"$regex": "\[住宿\].*(東京)+.*"}, "date": {"$gt": d_end}}
        ]
    }, no_cursor_timeout=True).batch_size(20)

    print('Total:', articles.count())
	
    i = 0
    tmp_data = {}
    for article in articles:
        #if i==7:
        #    break
        tmp_data[article['article_id']] = (article['article_title'], article['content'])
        print(i)
        #print(article, article['article_title'])
        print(article['article_title'])
        #print(article['content'])
        #print(article)
        if article['article_id'] in testing_corpus_data.keys():
            testing_corpus.append(testing_corpus_data[article['article_id']]['feature'])
            i = i+1
            continue
        else:
            doc = []
            doc += splitWord(article['article_title'])
            doc += splitWord(article['content'])
            testing_corpus_data[article['article_id']] = {
                'feature': doc,
                'topic': [],
				'index': i
            }
            testing_corpus.append(doc)
            i = i+1
        #input()
    t_end = time.time()
    write_json(testing_corpus_data, 'testing_corpus_data.json')
    print('time elapsed for building corpus: %f minutes' % ((t_end-t_start)/60.0))

    print('Inferring')
    category = load_json('category.json')
    dictionary = corpora.Dictionary.load('train.dict')
    corpus_bow = corpora.MmCorpus('train.mm')
    tfidf = models.TfidfModel.load('train.tfidf')
    lda = models.ldamodel.LdaModel.load('train.lda')
    index = similarities.MatrixSimilarity.load('train.index')
	
    training_corpus_data = load_json('corpus_data.json')

    for testing_aid in testing_corpus_data.keys():
        #print(testing_corpus_data[testing_aid]['feature'])
        print(testing_aid)
        vec_bow = dictionary.doc2bow(testing_corpus_data[testing_aid]['feature'])
        vec_tfidf = tfidf[vec_bow]
        vec_lda = lda[vec_tfidf]  # convert the query to LDA space
        sims = index[vec_lda]  # perform a similarity query against the corpus
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #print(sims)
        training_index = str(sims[0][0])
        for training_aid in training_corpus_data.keys():
            if str(training_corpus_data[training_aid]['index']) == training_index:
                testing_corpus_data[testing_aid]['topic'] = training_corpus_data[training_aid]['topic']
                #for t in testing_corpus_data[testing_aid]['topic']:
                    #print(category[t])
                break
    write_json(testing_corpus_data, 'testing_corpus_data_label.json')
	

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
