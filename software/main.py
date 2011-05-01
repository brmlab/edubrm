#!/usr/bin/python

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from mainUi import Ui_MainWindow

class ModuleButton(QPushButton):

    def __init__(self, mod, parent):
        super(ModuleButton, self).__init__(QIcon("modules/%s.png" % mod.__class__.__name__), mod.title, parent)
        self.setMinimumHeight(50)
        self.mod = mod
        self.form = parent
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        # reinit because of the widget
        self.mod.__init__()
        self.form.ui.areaChoose.hide()
        self.form.ui.btnExit.hide()
        self.form.ui.btnBack.show()
        self.form.ui.lblTitle.setText(self.mod.title)
        self.form.ui.areaModule.setWidget(self.mod.widget)
        self.form.ui.areaModule.show()
        self.form.mod = self.mod
        self.mod.start()

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnBack.hide()
        self.ui.areaModule.hide()
        self.addModuleButtons()

    @pyqtSlot()
    def on_btnExit_clicked(self):
        self.close()

    @pyqtSlot()
    def on_btnBack_clicked(self):
        self.mod.stop()
        self.ui.lblTitle.setText('EduBRM')
        self.ui.areaChoose.show()
        self.ui.areaModule.hide()
        self.ui.btnExit.show()
        self.ui.btnBack.hide()

    @pyqtSlot()
    def on_btnAbout_clicked(self):
        box = QMessageBox(QMessageBox.NoIcon, "About EduBRM", "EduBRM by Hackerspace brmlab\n\nhttp://brmlab.cz/\n\nSee README for more information.", QMessageBox.Ok, self)
        box.setIconPixmap(QPixmap( ":/icons/icon.png"))
        box.exec_()

    def addModuleButtons(self):
        import modules
        for mod in modules.list():
            c = self.ui.gridLayout.count()
            btn = ModuleButton(mod, self)
            self.ui.gridLayout.addWidget(btn, c / 2, c % 2)
