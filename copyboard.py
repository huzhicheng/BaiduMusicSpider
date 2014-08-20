# -*- coding:utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

import time

class linkboard(QtGui.QDialog):
    def __init__(self,args,parent=None):
        super(linkboard,self).__init__(parent)
        text = QtGui.QTextEdit()
        text.setText(args)
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.addWidget(text)
        self.setLayout(self.mainLayout)   