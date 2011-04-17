from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import QObject
from ModuleDebugUi import Ui_ModuleDebug

class ModuleDebugWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ModuleDebug()
        self.ui.setupUi(self)

class ModuleDebug():

    def __init__(self):
        self.title = 'Debug'
        self.widget = ModuleDebugWidget()

    def run(self):
        print 'run Debug'
