# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_history/ui\widget_history.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(640, 480)
        widget.setStyleSheet("")
        self.layout_history = QtWidgets.QHBoxLayout(widget)
        self.layout_history.setContentsMargins(0, -1, 0, 0)
        self.layout_history.setObjectName("layout_history")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.button_up = QtWidgets.QPushButton(widget)
        self.button_up.setObjectName("button_up")
        self.verticalLayout.addWidget(self.button_up)
        self.button_down = QtWidgets.QPushButton(widget)
        self.button_down.setObjectName("button_down")
        self.verticalLayout.addWidget(self.button_down)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.button_remove_all = QtWidgets.QPushButton(widget)
        self.button_remove_all.setObjectName("button_remove_all")
        self.verticalLayout.addWidget(self.button_remove_all)
        self.layout_history.addLayout(self.verticalLayout)
        self.list_widget = QtWidgets.QListWidget(widget)
        self.list_widget.setObjectName("list_widget")
        self.layout_history.addWidget(self.list_widget)

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Form"))
        self.button_up.setText(_translate("widget", "NACH OBEN"))
        self.button_down.setText(_translate("widget", "NACH UNTEN"))
        self.button_remove_all.setText(_translate("widget", "LÖSCHE HISTORY"))
