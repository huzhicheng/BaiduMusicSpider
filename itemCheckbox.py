#-*- coding:utf-8 -*-
'''
Created on 2014��2��21��

@author: huzhicheng
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import settings


class DelegateButton(QStyledItemDelegate):

    
    def paint(self, painter, option, index):
        starRating = index.data().toList()
        #s = QVariant(["ss","nn"])
        print settings.translate(starRating[0].toString())
        
        print starRating
        
#         if isinstance(starRating, StarRating):
#             if option.state & QtGui.QStyle.State_Selected:
#                 painter.fillRect(option.rect, option.palette.highlight())
# 
#             starRating.paint(painter, option.rect, option.palette,
#                     StarRating.ReadOnly)
#         else:
#             super(StarDelegate, self).paint(painter, option, index)

    def sizeHint(self, option, index):
        starRating = index.data()
#         if isinstance(starRating, StarRating):
#             return starRating.sizeHint()
#         else:
#             return super(StarDelegate, self).sizeHint(option, index)

    def createEditor(self, parent, option, index):
        starRating = index.data()
        btn = QPushButton("hhi",parent=parent)
        return btn
#         if isinstance(starRating, StarRating):
#             editor = StarEditor(parent)
#             editor.editingFinished.connect(self.commitAndCloseEditor)
#             return editor
#         else:
#             return super(StarDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        starRating = index.data()
#         if isinstance(starRating, StarRating):
#             editor.setStarRating(starRating)
#         else:
#             super(StarDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        starRating = index.data()
#         if isinstance(starRating, StarRating):
#             model.setData(index, editor.starRating())
#         else:
#             super(StarDelegate, self).setModelData(editor, model, index)

    def commitAndCloseEditor(self):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
    

        