#-*- coding:utf- 8 -*-
__author__ = 'huzhicheng'


import Queue
import time
import urllib2
import urllib
import cookielib
import settings
import threading
import logging
import os
import re
from bs4 import BeautifulSoup
import spiderWorker
import codecs
import sys

LOG_FILENAME = "/".join([os.path.dirname(__file__),"logon.log"])
logger = logging.getLogger()
handler = logging.FileHandler(LOG_FILENAME)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Helper(threading.Thread):
    def __init__(self):
        super(Helper,self).__init__()

    def run(self):
        if not self.login():
            print "登录失败"
            return False

        queue = Queue.Queue()

        pool = self.buildThreads(queue)

        req = urllib2.urlopen(settings.musiclistUrl)
        content = req.read()
        soup = BeautifulSoup(content)
        tags = soup.find_all("div",class_="song-item")
        for tag in tags:
            span = tag.find("span",class_="song-title")
            href = span.a["href"]
            if href.startswith("/song"):
                queue.put(href)

        for worker in pool:
            queue.put(u"quit")

        for worker in pool:
            worker.join()




    def buildThreads(self,queue):
        workers = []
        for i in range(9):
            worker = spiderWorker.worker(queue,"T"+str(i))
            worker.start()
            workers.append(worker)
        return workers


    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar=cj))
        urllib2.install_opener(opener)

        print "Get Cookie"
        logger.info("Get Cookie")
        url = "http://www.baidu.com"
        request = urllib2.Request(url)
        openRequest = urllib2.urlopen(request)
        for index,cookie in enumerate(cj):
            print "[%s]:%s\r\n" % (index,cookie)
            logger.info("{0}:{1}".format(index,cookie))

        print "Get token"
        logger.info("Get token")
        tokenUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
        tokenRequest = urllib2.urlopen(tokenUrl)
        tokenHtml = tokenRequest.read()
        #reg = re.compile(r"bdPass.api.params.login_token='\w+';")
        reg = re.compile(r"bdPass.api.params.login_token='(?P<tokenVal>\w+)';")
        token = reg.findall(tokenHtml)
        if token:
            tokenVal = token[0]
            print tokenVal
            logger.info(tokenVal)

        print "登录成功"
        logger.info("登录成功")
        baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login"
        print settings.username
        userInfo = {"userName":settings.username,"passWord":settings.password}
        postData =self.BuildPostData(tokenVal,userInfo)
        userAgent ="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36"
        #userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
        baiduRequest = urllib2.Request(baiduMainLoginUrl,postData,headers={"User-Agent":userAgent})
        openBaiduRequest = urllib2.urlopen(baiduRequest)
        baiduPage = openBaiduRequest.read()

        personCenter = urllib2.urlopen("http://i.baidu.com/")
        if personCenter.read().find("header-tuc-uname")>-1:
            print "Login OK Congratulation!"
            logger.info("Login OK Congratulation!")

        else:
            print "Login fail"
            logger.info("Login fail")
            return False


        #urlRe = re.compile("encodeURI\\('(?P<fzUrl>\s+)'\\);")
        urlRe = re.compile(r"(?P<URL>http://www.baidu.com/cache/user/html/jump.html\S+)'")
        #TODO:
        #urlRe = re.compile("window.location.replace\\(\\)")
        lastUrl = urlRe.findall(baiduPage)
        if lastUrl:
            print lastUrl[0]

        trueLoginUrl = lastUrl[0]

        lastRequest = urllib2.Request(trueLoginUrl)
        openLastRequest = urllib2.urlopen(trueLoginUrl)
        print openLastRequest.geturl()
        logger.info("真正登录地址：{0}".format(openLastRequest.geturl()))
        return True


    def BuildPostData(self,token,userInfo):
        jumppage = "http://www.baidu.com/cache/user/html/jump.html"

        postDict = {
            'charset':"utf-8",
            'token':token, #de3dbf1e8596642fa2ddf2921cd6257f
            'isPhone':"false",
            'index':"0",
            'staticpage':jumppage, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            'loginType':"1",
            'tpl':"mn",
            'callback':"parent.bdPass.api.login._postCallback",
            'username':userInfo["userName"],
            'password':userInfo["passWord"],
            'mem_pass':"on",}
        return  urllib.urlencode(postDict)

