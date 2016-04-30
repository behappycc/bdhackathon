import argparse

import pymongo
from pymongo import MongoClient

import jieba
import jieba.posseg as pseg


def main():
    parser = argparse.ArgumentParser(description='Find Stop Words')
    parser.add_argument('-b', metavar='BOARD_NAME', help='Board name', required=True)
    args = parser.parse_args()
    board = args.b

    client = MongoClient('localhost', 27017)
    collection = client['bdhackathon'][board]

    find_stop_words(collection)

def splitWord(sentence):
    if u']' in sentence:
        sentence = sentence.split("]", 1)[1]
    #print '---',sentence
    nWord = []
    for word, flag in pseg.cut(sentence):
        if(flag in ['n', 'v', 'a', 'ns', 'nt', 'nz']) and (len(word)>1):
            nWord.append(word)

    return nWord

def find_stop_words(collection):
    articles = collection.find()
    with open('test.txt', 'w') as datafile:
        for article in articles:
            key_word = []
            #title = article['article_title']
            content = article['content']
            print(content)
            key_word.append(splitWord(content))
            datafile.write(str(key_word))
            #datafile.write(',')
            datafile.write('\n')

if __name__ == '__main__':
    main()