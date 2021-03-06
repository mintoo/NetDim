# Copyright (C) 2017 Antoine Fourmy <antoine dot fourmy at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict
from miscellaneous.decorators import update_paths
from .napalm_functions import str_dict
from pyQT_widgets.Q_console_edit import QConsoleEdit
from PyQt5.QtWidgets import (
                             QGridLayout, 
                             QLabel, 
                             QListWidget,
                             QWidget
                             )

class NapalmGeneral(QWidget):
    
    # Facts and environment

    @update_paths
    def __init__(self, node, controller):
        super().__init__()
        self.node = node

        action_label = QLabel('Action')
        object_label = QLabel('Object')
        
        self.general_list = QListWidget()
        self.general_list.setSortingEnabled(True)
        self.general_list.itemSelectionChanged.connect(self.info_update)
        
        self.action_list = QListWidget()
        self.action_list.setSortingEnabled(True)
        self.action_list.itemSelectionChanged.connect(self.action_update)
        
        self.properties_edit = QConsoleEdit()
        self.properties_edit.setMinimumSize(300, 300)

        layout = QGridLayout()
        layout.addWidget(object_label, 0, 0)
        layout.addWidget(self.general_list, 1, 0)
        layout.addWidget(action_label, 0, 1)
        layout.addWidget(self.action_list, 1, 1)
        layout.addWidget(self.properties_edit, 2, 0, 1, 2)
        self.setLayout(layout)
        
    def update(self):
        self.general_list.clear()
        if 'Environment' in self.node.napalm_data:
            infos = ['Facts'] + list(self.node.napalm_data['Environment'])
            self.general_list.addItems(infos)
            
    def info_update(self):
        self.properties_edit.clear()
        info = self.general_list.currentItem().text()
        
        if info == 'Facts':
            value = str_dict(self.node.napalm_data['Facts'])
            self.properties_edit.insertPlainText(value)
        else:
            self.action_list.clear()
            values = map(str, self.node.napalm_data['Environment'][info])
            self.action_list.addItems(values)
            
    def action_update(self):
        self.properties_edit.clear()
        action = self.action_list.currentItem()
        if action:
            info = self.general_list.currentItem().text()
            action_dict = self.node.napalm_data['Environment'][info][action.text()]
            self.properties_edit.insertPlainText(str_dict(action_dict))
                        