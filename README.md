# bdhackathon
big data hackathon [link](http://www.bdhackathon.org.tw/).

## Installation
* Python3
* mongoDB ([install on Ubuntu 14.04](https://www.liquidweb.com/kb/how-to-install-mongodb-on-ubuntu-14-04/), [GUI](http://edgytech.com/umongo/))

Dump and restore
```
mongodump --db DataBaseName
mongorestore --db DataBaseName /path/to/DataBaseName
```
Note that /path/to/DataBaseName should be a directory filled with .json and .bson representations of your data

* pip install -r requirement.txt

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
