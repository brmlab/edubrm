from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QTimer
from ModuleBUi import Ui_ModuleB
from device import Device

class ModuleBWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ModuleB()
        self.ui.setupUi(self)

        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.read_inputs)

        self.scene_nobat = QGraphicsScene()
        self.scene_nobat.addPixmap(QPixmap('modules/ModuleB-nobat.png'))
        self.scene_off = QGraphicsScene()
        self.scene_off.addPixmap(QPixmap('modules/ModuleB-off.png'))
        self.scene_on = QGraphicsScene()
        self.scene_on.addPixmap(QPixmap('modules/ModuleB-on.png'))
        self.ui.widgetImg.setScene(self.scene_nobat)

    def read_inputs(self):
        r = self.dev.read()
        us = r[1]/1023.0 * 3.3 - 0.095
        if us < 0.0:
            us = 0.0
        uc = r[2]/1023.0 * 3.3 - 0.04
        if uc < 0.0:
            uc = 0.0
        i = (us-uc)/18*1000
        if i < 0.0 or uc == 0.0:
            i = 0.0
        self.ui.labelUs.setText('Us = %0.3f V' % us)
        self.ui.labelUc.setText('Uc = %0.3f V' % uc)
        self.ui.labelI.setText('I = %0.2f mA' % i)
        if us < 1.5:
            self.ui.widgetImg.setScene(self.scene_nobat)
        else:
            if uc < 1:
                self.ui.widgetImg.setScene(self.scene_off)
            else:
                self.ui.widgetImg.setScene(self.scene_on)

class ModuleB():

    def __init__(self):
        self.title = 'Simple DC circuit'
        self.widget = ModuleBWidget()

    def start(self):
        self.widget.dev = Device()
        self.widget.timer.start(50)

    def stop(self):
        self.widget.timer.stop()
