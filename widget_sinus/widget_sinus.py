#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from model.data import data
from widget_base import SubWidgetBase, WidgetBase
from widget_history.ui.widget_history import Ui_widget
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox


class WidgetHistory(SubWidgetBase):
    OBJECT_NAME = 'WidgetHistory'

    def __init__(self, main_window):
        super().__init__(main_window)
        self.ui = Ui_widget()
        self.ui.setupUi(self)
        self.setObjectName(WidgetHistory.OBJECT_NAME + '_{:d}'.format(WidgetBase.counter))

        self.data_update_sender = False

        self.ui.button_up.clicked.connect(self.on_button_up)
        self.ui.button_down.clicked.connect(self.on_button_down)
        self.ui.button_remove_all.clicked.connect(self.on_button_remove_all)
        self.ui.list_widget.itemDoubleClicked.connect(self.on_list_item_double_clicked)

    def on_list_item_double_clicked(self, item  # type: QListWidgetItem
                             ):
        pos_spec_char = item.text().find('{ ')
        text = item.text()[:(pos_spec_char - 1)]
        data.osm_search = text
        self.data_update_sender = True
        data.callback_update()

    def on_button_up(self):
        current_row = self.ui.list_widget.currentRow()
        if current_row > 0:
            item = self.ui.list_widget.takeItem(current_row)
            self.ui.list_widget.insertItem(current_row - 1, item)
            self.ui.list_widget.setCurrentRow(current_row - 1)
        else:
            if current_row == (-1):
                QMessageBox.about(self, ' ', 'Kein Element selektiert')
            else:
                QMessageBox.about(self, ' ', 'Element kann nicht weiter verschoben werden')

    def on_button_remove_all(self):
        for i in range(self.ui.list_widget.count()):
            self.ui.list_widget.takeItem(0)

    def on_button_down(self):
        current_row = self.ui.list_widget.currentRow()
        if current_row < (self.ui.list_widget.count() - 1):
            item = self.ui.list_widget.takeItem(current_row)
            self.ui.list_widget.insertItem(current_row + 1, item)
            self.ui.list_widget.setCurrentRow(current_row + 1)
        else:
            if current_row == (-1):
                QMessageBox.about(self, ' ', 'Kein Element selektiert')
            else:
                QMessageBox.about(self, ' ', 'Element kann nicht weiter verschoben werden')

    def timestamp(self):
        now = time.time()
        localtime = time.localtime(now)
        milliseconds = '%03d' % int((now - int(now)) * 1000)
        return time.strftime('%H:%M:%S.', localtime) + milliseconds

    def callback_data_update(self):
        if self.data_update_sender:
            self.data_update_sender = False
        else:
            msg = data.osm_search + ' { ' + self.timestamp() + ' | ' + \
                  'zl = {:d}'.format(data.osm_zoom_level) + ' }'

            self.ui.list_widget.setCurrentRow(0)
            self.ui.list_widget.insertItem(self.ui.list_widget.currentRow(), msg)
            self.ui.list_widget.setCurrentRow(0)
