#-*- coding:utf-8 -*-
__author__ = 'huzhicheng'

import threading
from threading import RLock
import urllib2
from bs4 import BeautifulSoup
import codecs
import os

root = os.path.dirname(__file__)+"/"

lock = RLock()

class worker(threading.Thread):
    def __init__(self,queue,tname):
        super(worker,self).__init__(name=tname)
        self._queue = queue

    def run(self):
        while True:
            lock.acquire()
            mLink = self._queue.get()
            lock.release()
            if isinstance(mLink,unicode) and mLink=="quit":
                break
            downloadUrl = "http://music.baidu.com"+mLink+"/download"
            req = urllib2.urlopen(downloadUrl)
            soup = BeautifulSoup(req.read())
            tag = soup.find("a",id="128")
            if tag:
                print(threading.currentThread().getName(),tag["href"])
                songNameSoup = soup.find("a",class_="song-link-hook")
                if songNameSoup:
                    name = songNameSoup.text
                    name = unicode(name).encode("utf-8")
                singerSoup = soup.find("span",class_="author_list")
                if singerSoup:
                    author = singerSoup["title"]
                    author= unicode(author).encode("utf-8")
                record = "|".join(["http://music.baidu.com"+unicode(tag["href"]).encode("utf-8"),name,author])
                lock.acquire()
                f = codecs.open(root+"list.txt","a")
                f.write(record+"\n")
                f.close()
                lock.release()







