# -*- coding: utf-8 -*-

'''
Created on 2014��2��26��

@author: huzhicheng
'''
from PyQt4 import QtGui,QtCore

class fzDownloadButton(QtGui.QPushButton):
    '''
    classdocs
    '''


    def __init__(self,rowNum,columnNum,parent=None):
        super(fzDownloadButton,self).__init__(parent) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('''QPushButton{background-image:url(./img/downloads.png);width:27px;height:28px;padding:0px;border:0px;}''')
        self.clicked.connect(self.emitClickWithParam)
        self.row = rowNum
        self.column = columnNum
        
    def emitClickWithParam(self):
        self.emit(QtCore.SIGNAL("downloadclick(int,int)"),self.row ,self.column)
        