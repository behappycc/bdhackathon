#coding=utf-8

#python native module
import os
import re

#whoosh module
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser

#jeiba module
from jieba.analyse import ChineseAnalyzer
import jieba
jieba.load_userdict("japan_dict.txt")
analyzer = ChineseAnalyzer()

#mongodb module
import pymongo
from pymongo import MongoClient

#custom files

def build_index():
    print("build index")
    client = MongoClient('localhost', 27017)
    collection = client['bdhackathon']['Japan_Travel']
    schema = Schema(
        article_title=TEXT(stored=True, analyzer=analyzer), 
        article_id=TEXT(stored=True),
        author=TEXT(stored=True),
        #content=TEXT(stored=True, analyzer=analyzer)
        )

    #Initial Whoosh index
    if not os.path.exists("index"):
        os.mkdir("index")
        create_in("index", schema)

    ix = open_dir("index")
    writer = ix.writer()
    articles = collection.find()
    for article in articles:
        writer.update_document(
            article_title = article["article_title"],
            article_id = article["article_id"],
            author = article["author"]["account"],
            #content= article["content"]
            )
    writer.commit()

def search_article(query):
    print("search")
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query = MultifieldParser(["article_title", "article_id", "author"], ix.schema).parse(query)
        results = searcher.search(query, limit=None)
        with open('test.txt', 'w') as datafile:
            print(len(results))
            datafile.write(str(results[11]))
            '''
            for result in results:
                rs = result["article_title"] + " " +result["article_id"] + " " + result["author"]
                datafile.write(rs)
                datafile.write("\n")
                print(result["article_title"], result["article_id"], result["author"])
            '''
def main():
    build_index()
    search_article("大阪")

if __name__ == '__main__':
    main()