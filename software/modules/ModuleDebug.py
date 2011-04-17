from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot
from ModuleDebugUi import Ui_ModuleDebug
#from device import Device

class ModuleDebugWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ModuleDebug()
        self.ui.setupUi(self)
#        self.dev = Device()

    @pyqtSlot(int)
    def on_dialPWM1_valueChanged(self, val):
#        self.dev.pwm(1, val)
        print 'pwm1:', val

    @pyqtSlot(int)
    def on_dialPWM2_valueChanged(self, val):
#        self.dev.pwm(2, val)
        print 'pwm2:', val

    @pyqtSlot(int)
    def on_dialAMP1_valueChanged(self, val):
#        self.dev.opamp(1, val)
        print 'amp1:', val

    @pyqtSlot(int)
    def on_dialAMP2_valueChanged(self, val):
#        self.dev.opamp(2, val)
        print 'amp2:', val

    @pyqtSlot(int)
    def on_checkOut0_stateChanged(self, state):
#        state and self.dev.setout(1<<0) or self.dev.clrout(1<<0)
        print 'out0:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut1_stateChanged(self, state):
#        state and self.dev.setout(1<<1) or self.dev.clrout(1<<1)
        print 'out1:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut2_stateChanged(self, state):
#        state and self.dev.setout(1<<2) or self.dev.clrout(1<<2)
        print 'out2:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut3_stateChanged(self, state):
#        state and self.dev.setout(1<<3) or self.dev.clrout(1<<3)
        print 'out3:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut4_stateChanged(self, state):
#        state and self.dev.setout(1<<4) or self.dev.clrout(1<<4)
        print 'out4:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut5_stateChanged(self, state):
#        state and self.dev.setout(1<<5) or self.dev.clrout(1<<5)
        print 'out5:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut6_stateChanged(self, state):
#        state and self.dev.setout(1<<6) or self.dev.clrout(1<<6)
        print 'out6:', state and '1' or '0'

    @pyqtSlot(int)
    def on_checkOut7_stateChanged(self, state):
#        state and self.dev.setout(1<<7) or self.dev.clrout(1<<7)
        print 'out7:', state and '1' or '0'

class ModuleDebug():

    def __init__(self):
        self.title = 'Debug'
        self.widget = ModuleDebugWidget()

    def run(self):
        print 'run Debug'
