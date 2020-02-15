# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\old_main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_ui(object):
    def setupUi(self, main_ui):
        main_ui.setObjectName("main_ui")
        main_ui.resize(500, 250)
        self.central_widget = QtWidgets.QWidget(main_ui)
        self.central_widget.setObjectName("central_widget")
        main_ui.setCentralWidget(self.central_widget)

        self.retranslateUi(main_ui)
        QtCore.QMetaObject.connectSlotsByName(main_ui)

    def retranslateUi(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.setWindowTitle(_translate("main_ui", "windowTitle"))


