from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QTimer
from ModuleCUi import Ui_ModuleC
from device import Device

class ModuleCWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ModuleC()
        self.ui.setupUi(self)

        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.read_inputs)

    def read_inputs(self):
        pass
#        r = self.dev.read()
#        v = r[0]/1023.0 * 3.3
#        self.ui.labelV.setText('{:0.3f} V'.format(v))
#        self.ui.progressV.setValue(1000*v)

class ModuleC():

    def __init__(self):
        self.title = 'L/C/LC circuit'
        self.widget = ModuleCWidget()

    def start(self):
        self.widget.dev = Device()
        self.widget.timer.start(50)

    def stop(self):
        self.widget.timer.stop()
