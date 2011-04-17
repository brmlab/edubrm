from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from ModuleDebugUi import Ui_ModuleDebug
#from device import Device

class ModuleDebugWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ModuleDebug()
        self.ui.setupUi(self)
        QObject.connect(self.ui.comboAMP1c, SIGNAL("currentIndexChanged(int)"), self.on_comboAMP1_changed)
        QObject.connect(self.ui.comboAMP1g, SIGNAL("currentIndexChanged(int)"), self.on_comboAMP1_changed)
        QObject.connect(self.ui.comboAMP2c, SIGNAL("currentIndexChanged(int)"), self.on_comboAMP2_changed)
        QObject.connect(self.ui.comboAMP2g, SIGNAL("currentIndexChanged(int)"), self.on_comboAMP2_changed)
        QObject.connect(self.ui.pushSwitch1, SIGNAL("clicked(bool)"), self.on_switches_changed)
        QObject.connect(self.ui.pushSwitch2, SIGNAL("clicked(bool)"), self.on_switches_changed)
        QObject.connect(self.ui.pushSwitch3, SIGNAL("clicked(bool)"), self.on_switches_changed)
        QObject.connect(self.ui.pushSwitch4, SIGNAL("clicked(bool)"), self.on_switches_changed)
        QObject.connect(self.ui.pushSwitch5, SIGNAL("clicked(bool)"), self.on_switches_changed)
        QObject.connect(self.ui.pushSwitch6, SIGNAL("clicked(bool)"), self.on_switches_changed)
        QObject.connect(self.ui.pushPin1, SIGNAL("clicked(bool)"), self.on_pins_changed)
        QObject.connect(self.ui.pushPin2, SIGNAL("clicked(bool)"), self.on_pins_changed)
        QObject.connect(self.ui.pushPin3, SIGNAL("clicked(bool)"), self.on_pins_changed)

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

    @pyqtSlot(bool)
    def on_radioSine_clicked(self, checked):
#        self.dev.ddswave(0)
        print 'dds: sine'

    @pyqtSlot(bool)
    def on_radioSquare_clicked(self, checked):
#        self.dev.ddswave(1)
        print 'dds: square'

    @pyqtSlot(bool)
    def on_radioSaw_clicked(self, checked):
#        self.dev.ddswave(2)
        print 'dds: saw'

    @pyqtSlot(bool)
    def on_radioInvSaw_clicked(self, checked):
#        self.dev.ddswave(3)
        print 'dds: invsaw'

    @pyqtSlot(int)
    def on_dialDDS_valueChanged(self, val):
#        self.dev.ddsfreq(val)
        print 'dds:', val

    @pyqtSlot()
    def on_comboAMP1_changed(self):
        c = self.ui.comboAMP1c.currentIndex() + 1
        g = (1,2,4,5,8,10,16,32)[self.ui.comboAMP1g.currentIndex()]
#        self.dev.opamp(1, c, g)
        print 'amp1:', c, g

    @pyqtSlot()
    def on_comboAMP2_changed(self):
        c = self.ui.comboAMP2c.currentIndex() + 1
        g = (1,2,4,5,8,10,16,32)[self.ui.comboAMP2g.currentIndex()]
#        self.dev.opamp(2, c, g)
        print 'amp2:', c, g

    @pyqtSlot()
    def on_switches_changed(self):
        s = (self.ui.pushSwitch1.isChecked() and 1 or 0,
             self.ui.pushSwitch2.isChecked() and 1 or 0,
             self.ui.pushSwitch3.isChecked() and 1 or 0,
             self.ui.pushSwitch4.isChecked() and 1 or 0,
             self.ui.pushSwitch5.isChecked() and 1 or 0,
             self.ui.pushSwitch6.isChecked() and 1 or 0)
#        self.dev.switches(s[0] + s[1]<<1 + s[2]<<2 + s[3]<<3 + s[4]<<4 + s[5]<<5)
        print 'switches:', s

    @pyqtSlot()
    def on_pins_changed(self):
        s = (self.ui.pushPin1.isChecked() and 1 or 0,
             self.ui.pushPin2.isChecked() and 1 or 0,
             self.ui.pushPin3.isChecked() and 1 or 0)
        self.ui.pushOut1.setEnabled(not s[0])
        self.ui.pushOut2.setEnabled(not s[1])
        self.ui.pushOut3.setEnabled(not s[2])
#        self.dev.setpins(s[0] + s[1]<<1 + s[2]<<2)
        print 'pins:', s

    @pyqtSlot(bool)
    def on_pushOut1_clicked(self, checked):
#        self.dev.setout(1, checked and 1 or 0)
        print 'out1:', checked and 1 or 0

    @pyqtSlot(bool)
    def on_pushOut2_clicked(self, checked):
#        self.dev.setout(2, checked and 1 or 0)
        print 'out2:', checked and 1 or 0

    @pyqtSlot(bool)
    def on_pushOut3_clicked(self, checked):
#        self.dev.setout(3, checked and 1 or 0)
        print 'out3:', checked and 1 or 0

    @pyqtSlot(int)
    def on_dialInputFreq_valueChanged(self, val):
# TODO: change sampling rate to (val) freq
        print 'inputfreq:', val

class ModuleDebug():

    def __init__(self):
        self.title = 'Debug'
        self.widget = ModuleDebugWidget()

    def run(self):
        print 'run Debug'
