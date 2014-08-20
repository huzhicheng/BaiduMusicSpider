#-*- coding:utf-8 -*-
__author__ = 'huzhicheng'

import threading
import dispatcher
import urllib2
import urllib
import os
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
from itemCheckbox import *
import codecs
from random import randint
from downloadPushbutton import *
import settings
from threading import Thread, RLock
from Queue import Queue
from copyboard import linkboard

root = os.path.dirname(__file__)+"/"


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#主窗体
class Ui_MainWindow(QtGui.QDialog):

    #===========================================================================
    # 配置文件路径
    #===========================================================================
    CONFIGPATH = os.getcwd()+"\config"

    #===========================================================================
    # 歌曲默认保存位置
    #===========================================================================
    DEFAUTMUSICPATH = os.getcwd()+"\music"
    #===========================================================================
    # 标识是否继续下载 用于批量下载
    #===========================================================================
    continueDownload = True

    #===========================================================================
    # 待下载歌单队列
    #===========================================================================
    songsMenu = None

    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__(parent)

        #如果不存在默认保存位置 则创建路径
        try:
            if not os.path.exists(self.DEFAUTMUSICPATH):
                os.mkdir(self.DEFAUTMUSICPATH)
        except:raise
        #初始化歌曲存储位置
        self.stroagePath = self.getDefaultStroagePath()
        self.dragPosition = None
        if settings.username=="" or settings.username=="your baidu acount" \
        or settings.password=="" or settings.password=="your baidu password":
            print "Please setting your username and password"
            return

        #初始化UI
        self.setupUi(self)
        #self.settingWindow = settingDig(self)



    #初始化歌曲存储位置 如果是第一次使用 则创建配置文件 否则读取配置文件中保存的歌曲保存路径
    def getDefaultStroagePath(self):
        sPath = self.DEFAUTMUSICPATH
        try:
            if not os.path.exists(self.CONFIGPATH):
                os.mkdir(self.CONFIGPATH)
            else:
                f = codecs.open(self.CONFIGPATH+"\config.ini","r","utf-8")
                sPath = f.read()
                print(sPath)
        except:
            sPath = self.DEFAUTMUSICPATH
        return sPath

    #加载歌单显示区域
    def createDataWidget(self):
        if not settings.recordsExistAndLasted():
            starttime = time.time()
            dispatch = dispatcher.Helper()
            dispatch.start()
            dispatch.join()
            print(u"耗时{0}".format(time.time()-starttime))

        songlist=codecs.open(root+"list.txt")
        songlines = songlist.readlines()
        rowcount = len(songlines)
        print rowcount

        table = QTableWidget(rowcount,6)
        table.setEditTriggers(
            QtGui.QAbstractItemView.DoubleClicked |
            QtGui.QAbstractItemView.SelectedClicked)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        table.setHorizontalHeaderLabels([u"歌名",u"歌手",u'url',u"", u'',''])

        rowNumber = 0
        for info in songlines:
            url,song,singer = info.split("|")
            item1 = QTableWidgetItem(settings.translate(song))
            item2 = QTableWidgetItem(settings.translate(singer))
            item3 = QTableWidgetItem(settings.translate(url))
            item4 = QTableWidgetItem()
            item4.setCheckState(0)

            #item4.setCheckable(True)
            item5 = QTableWidgetItem()
            #item5.setData(0, [song,singer,url])

            item6Progress = QTableWidgetItem()


            #item5.setData(0,True)
            table.setItem(rowNumber,0,item1)
            table.setItem(rowNumber,1,item2)
            table.setItem(rowNumber,2,item3)
            table.setItem(rowNumber,3,item4)
            table.setItem(rowNumber,4,item5)
            table.setItem(rowNumber,5,item6Progress)

            btn = fzDownloadButton(parent=table,rowNum=rowNumber,columnNum=4)
            table.setCellWidget(rowNumber,4,btn)

            #下载进度条
            progressBar = QtGui.QProgressBar()
            progressBar.setVisible(False)
            progressBar.setMaximum(100)

            progressBar.setStyleSheet('''QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}
                                         QProgressBar::chunk {background-color: #05B8CC;width: 10px;margin:0.5px;}''')
            table.setCellWidget(rowNumber,5,progressBar)

            table.connect(btn,SIGNAL("downloadclick(int , int)"),self.downLoad_click_thread)

            rowNumber+=1


        table.resizeColumnsToContents()
        table.setColumnHidden(2,True)
        table.setGeometry(80, 20, 400, 300)
        songlist.close()
        table.setObjectName(_fromUtf8("tableView"))
        return table



    def downloadCallback(self,a,b,c):
        QApplication.processEvents()
        per=100*a*b/c
        if per>100:
            per = 100
        self.table.cellWidget(self.curDownloadRowNum, 5).setValue(per)

    curDownloadRowNum = 0
    def downLoad_click(self,row,column):
        songTitle =self.table.item(row, 0).text()
        singer = self.table.item(row, 1).text()
        songUrl = self.table.item(row, 2).text()

        #QtGui.QMessageBox.information(None, u"tips",u"%s，%s,%s" % (songTitle,singer,songUrl))
        self.curDownloadRowNum = row
        localPath ="%s%s%s" % (self.stroagePath+"/",unicode(songTitle).strip(),".mp3")
        print songUrl,localPath
        urllib.urlretrieve(str(songUrl), localPath, self.downloadCallback)

    def downLoad_click_thread(self,row,column):
        songTitle =self.table.item(row, 0).text()
        singer = self.table.item(row, 1).text()
        songUrl = self.table.item(row, 2).text()

        self.curDownloadRowNum = row
        localPath ="%s%s%s" % (self.stroagePath+"/",unicode(songTitle).strip(),".mp3")
        print songUrl,localPath
        #urllib.urlretrieve(str(songUrl), localPath, self.downloadCallback)
        self.lock = RLock()
        thread = Thread(target=self.download(songUrl,localPath))
        thread.setDaemon(True)
        thread.start()

    def download(self,songUrl,localPath):
        try:
            urllib.urlretrieve(str(songUrl),localPath,self.downloadCallback)
        except:pass




    def batchdownload_click(self):
        self.sender().setEnabled(False)
        threadNum = 5 #开启下载的线程数
        self.songsMenu = Queue()
        self.lock = RLock()
        rowCount = self.table.rowCount()
        for row in range(rowCount):
            if self.table.item(row, 3).checkState()>0: #获取地4列的内容 直接当做QChecbox使用
                #添加到批量下载歌单中：[[歌名,歌手,url],[歌名,歌手,url]] 可以复制所有链接 粘贴到迅雷等下载工具中 批量下载
                #songsMenu.append([self.table.item(row, 0).text(),self.table.item(row, 1).text(),self.table.item(row, 2).text()])
                #self.table.cellWidget(row, 4).click() #模拟点击下载按钮
                self.songsMenu.put([self.table.item(row, 0).text(),self.table.item(row, 1).text(),self.table.item(row, 2).text(),row])
        pool = []
        for _ in range(threadNum):
            pool.append(Thread(target=self.batchdownload()))
            pool[-1].setDaemon(True)
            pool[-1].start()


    def batchdownload(self):
        while not self.songsMenu.empty():
            self.lock.acquire()
            songinfo = self.songsMenu.get()
            self.lock.release()
            songTitle = songinfo[0]
            singer = songinfo[1]
            url = songinfo[2]
            row = songinfo[3]
            self.curDownloadRowNum = row
            s = unicode(songTitle)
            localPath ="%s%s%s" % (self.stroagePath+"/",s.strip(),".mp3")
            print localPath
            self.download(url, localPath)
            #self.songsMenu.task_done()
        else:
            self.btn_batchDownload.setEnabled(True)

    def copyToBoard(self):
        rowCount = self.table.rowCount()
        urls = []
        for row in range(rowCount):
            if self.table.item(row, 3).checkState()>0:
                urls.append(str(self.table.item(row, 2).text()))
        print urls
        board = linkboard(' '.join(urls))
        board.exec_()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(767, 584)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint| Qt.Dialog)

        #=======================================================================
        # 顶部操作栏
        #=======================================================================
        self.btn_close = QPushButton()
        self.connect(self.btn_close, SIGNAL("clicked()"),self.exitMianwindow)
        self.btn_close.setStyleSheet("""QPushButton{background-image:url(./img/btn_close_normal.png);width:39px;height:18px;padding-top:0px;border:0px;}
                                    QPushButton:hover{background-image:url(./img/btn_close_highlight.png);}
                                    QPushButton:pressed{background-image:url(./img/btn_close_down.png);}""")

        self.btn_min = QPushButton()
        self.connect(self.btn_min, SIGNAL("clicked()"),self.minWindow)
        self.btn_min.setStyleSheet("QPushButton{background-image:url(./img/btn_close_normal1.png);width:39px;height:18px;padding-top:0px;border:0px;}")

        self.btn_setting = QPushButton()
        self.connect(self.btn_setting,SIGNAL("clicked()"),self.setting_click)
        self.btn_setting.setStyleSheet("""QPushButton{background-image:url(./img/icon_cog.png);width:16px;height:16px;padding-top:0px;border:0px;margin-right:15px;}
                                        QPushButton:hover{background-image:url(./img/icon_cogs.png);}""")

        self.btn_photo = QPushButton()
        self.btn_photo.setStyleSheet("""QPushButton{background-image:url(./img/photo.png);width:32px;height:32px; border-radius: 10px;
                                        margin-right:15px;}""")

        self.topBarLayout = QtGui.QHBoxLayout()
        self.topBarLayout.addStretch()
        self.topBarLayout.addWidget(self.btn_photo,0,Qt.AlignRight | Qt.AlignHCenter)
        self.topBarLayout.addWidget(self.btn_setting,0,Qt.AlignRight | Qt.AlignHCenter)
        self.topBarLayout.addWidget(self.btn_min,0,Qt.AlignRight | Qt.AlignTop)
        self.topBarLayout.addWidget(self.btn_close,0,Qt.AlignRight | Qt.AlignTop)

        #=======================================================================
        # 列表区域  TODO:加载歌单列表之前会检查当前是否是登录用户
        #=======================================================================
        self.table = self.createDataWidget()
        #self.table.setStyleSheet("QWidget{background:url(./img/mianbg.png);}")
        self.listLayout = QtGui.QHBoxLayout()
        self.listLayout.addWidget(self.table)

        #=======================================================================
        # 底部操作栏
        #=======================================================================
        self.btn_batchDownload = QtGui.QPushButton(u"批量下载")
        self.connect(self.btn_batchDownload, SIGNAL('clicked()'),self.batchdownload_click)
        self.btn_copytoboard = QtGui.QPushButton(u"复制链接")
        self.connect(self.btn_copytoboard,SIGNAL("clicked()"),self.copyToBoard)
        self.btn_copytoboard.setToolTip(u"利用复制链接功能，将所选歌曲链接复制到剪切板，可在下载工具（如迅雷）中新建任务，直接粘贴即可实现批量下载。")
        self.checkall = QtGui.QCheckBox(u'全选')
        self.connect(self.checkall,SIGNAL("stateChanged(int)"),self.checkall_click)

        self.bottomBarLayout = QtGui.QHBoxLayout()
        self.bottomBarLayout.addStretch()
        self.bottomBarLayout.addWidget(self.checkall,0,Qt.AlignRight)
        self.bottomBarLayout.addWidget(self.btn_copytoboard,0,Qt.AlignRight)
        self.bottomBarLayout.addWidget(self.btn_batchDownload,0,Qt.AlignRight)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.topBarLayout,0)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.listLayout,1)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.bottomBarLayout,1)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)


    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        if event.button()==Qt.RightButton:
            self.close()

    def mouseMoveEvent(self,event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()

    def paintEvent(self,event):
        self.painter = QtGui.QPainter()
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), QPixmap("./img/mianbg.png"))
        self.painter.end()
    def checkall_click(self,state):
        rowCount = self.table.rowCount()
        if state==2:
            for i in range(rowCount):
                self.table.item(i, 3).setCheckState(2)
        else:
            for i in range(rowCount):
                self.table.item(i, 3).setCheckState(False)

    def setting_click(self):
        self.settingWindow = settings.settingDig(self.stroagePath,parent=self)
        self.settingWindow.show()

    def minWindow(self):
        self.showMinimized()

    def exitMianwindow(self):
        sys.exit(0)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "百度音乐下载器 ", None))
        self.label.setText(_translate("MainWindow", "头像", None))
        self.label_2.setText(_translate("MainWindow", "登录名称", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    loaderWindow = Ui_MainWindow()
    loaderWindow.show()
    sys.exit(app.exec_())





