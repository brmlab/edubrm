#!/usr/bin/python

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from mainUi import Ui_MainWindow

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        box = QMessageBox(QMessageBox.NoIcon, "About EduBRM", "EduBRM by Hackerspace brmlab\n\nhttp://brmlab.cz/\n\nSee README for more information.", QMessageBox.Ok)
        box.setIconPixmap(QPixmap( ":/icons/icon.png"))
        box.exec_()
