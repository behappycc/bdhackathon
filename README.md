# bdhackathon
big data hackathon [link](http://www.bdhackathon.org.tw/).

## Installation
1. Python3
2. Tornado
3. mongoDB
4. pymongo
5. gensim

##Coding Style
Google Python Style Guide [link](https://google.github.io/styleguide/pyguide.html).

##Usage
### Web Server
```
$ git clone https://github.com/behappycc/bdhackathon.git
$ cd bdhackathon/web
$ python3 Server.py -p 8888
```

### Data Analysis
```
$ cd bdhackathon/web
$ python3 ptt_crawler.py -b Japan_Travel -l
$ python3 topic_analyze.py -b Japan_Travel
$ python3 topic_label.py -b Japan_Travel 
```
After training LDA model(topic_analyze.py), user need to use topic_weight.txt to set up topic.txt.