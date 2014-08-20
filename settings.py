#-*- coding:utf-8 -*-
__author__ = 'huzhicheng'

from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import codecs,sys,os
import time

#username = "your baidu acount"    #配置你的百度账号
#password = "your baidu password"  #配置你的百度密码


musiclistUrl = "http://music.baidu.com/top/new"  #   http://music.baidu.com/top/new

root = os.path.dirname(__file__)+"/"

def translate(text):
        _encoding = QApplication.UnicodeUTF8
        return QApplication.translate("MainWindow", text, None, _encoding)


def lastModifyTimeIsToday(filename):
        '''
        判断最后修改时间是不是今天
        '''
        lastModifytime = time.strftime("%Y%m%d",time.localtime(os.stat(filename).st_mtime))
        timenow=time.strftime("%Y%m%d",time.localtime(time.time()))
        return lastModifytime==timenow

def recordsExistAndLasted():
        '''
        判断需要的文件是不是存在  并且是今天产生的
        '''
        listFile = root+"list.txt"

        if os.path.exists(listFile)  and \
        lastModifyTimeIsToday(listFile):
            return True
        else:
            return False

class settingDig(QtGui.QDialog):
    def __init__(self,argv='',parent=None):
        super(settingDig,self).__init__(parent)
        self.resize(QtCore.QSize(378,292))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)


        self.btn_close = QtGui.QPushButton()
        self.btn_close.setStyleSheet("""QPushButton{background-image:url(./img/btn_close_normal.png);width:39px;height:18px;padding-top:0px;border:0px;}
                                    QPushButton:hover{background-image:url(./img/btn_close_highlight.png);}
                                    QPushButton:pressed{background-image:url(./img/btn_close_down.png);}""")


        self.layout_top = QtGui.QHBoxLayout() #顶部栏
        #self.layout_top.addWidget(self.label_title,1,QtCore.Qt.AlignLeft)
        self.layout_top.addWidget(self.btn_close,0,QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        self.label_loginname = QtGui.QLabel(u"存储路径：")
        self.label_loginname.setMargin(10)
        self.text_storage = QtGui.QLineEdit()

        self.text_storage.setText(argv)
        self.text_storage.setFixedSize(230,30)
        self.btn_settingStoragePath = QtGui.QPushButton(u"请选择")
        self.btn_settingStoragePath.setStyleSheet("""QPushButton{background-image:url(./img/btn_ok.png);width:90px;height:25px;padding-top:0px;border:0px;}
            """)
        self.connect(self.btn_settingStoragePath,QtCore.SIGNAL("clicked()"),self.settingStorage_click)

        self.layout_loginname = QtGui.QVBoxLayout()
        self.layout_title = QtGui.QHBoxLayout()
        self.layout_loginname.addStretch()

        self.layout_loginname.addWidget(self.label_loginname)
        self.layout_title.addWidget(self.text_storage)
        self.layout_loginname.addStretch()
        self.layout_title.addWidget(self.btn_settingStoragePath)
        self.layout_loginname.addLayout(self.layout_title)



        self.btnOk = QtGui.QPushButton(u"保存")
        self.btnOk.setFixedSize(120,30)

        self.layout_button = QtGui.QHBoxLayout()
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.btnOk)
        self.layout_button.addStretch(1)



        self.layout_main = QtGui.QVBoxLayout() #整个布局外框
        self.layout_main.addLayout(self.layout_top)
        self.layout_main.addStretch() #平均分配空间
        self.layout_main.addLayout(self.layout_loginname)
        self.layout_main.addStretch() #平均分配空间

        self.layout_main.addLayout(self.layout_button)
        self.layout_main.addStretch() #平均分配空间
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(0,0,0,0)
        self.layout_main.setSpacing(0)

        self.connect(self.btn_close, QtCore.SIGNAL("clicked()"),self.LoginExit)
        self.connect(self.btnOk, QtCore.SIGNAL("clicked()"),self.setStorePath)


    def paintEvent(self,event):
        self.painter = QtGui.QPainter()
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), QtGui.QPixmap("./img/show_con_bg.jpg"))
        self.painter.end()


    def settingStorage_click(self):
        folder = QtGui.QFileDialog.getExistingDirectory(None,u"默认存储",os.getcwd())
        self.text_storage.setText(folder)


    def LoginExit(self):
        self.close()

    def setStorePath(self):
        storagepath = self.text_storage.text()
        storagepath = unicode(storagepath).encode("utf-8")
        print(storagepath)
        if not os.path.exists(storagepath):
            try:
                os.mkdir(storagepath)
            except:
                QtGui.QMessageBox.warning(self, u'路径错误', u'非法路径')
                return

        iniconfig = codecs.open(os.getcwd()+"\config"+"\config.ini","w")
        iniconfig.write(storagepath)
        iniconfig.close()
        self.parent().stroagePath = storagepath

        self.close()


