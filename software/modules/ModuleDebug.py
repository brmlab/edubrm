from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QPainterPath
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QColor
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QTimer
from ModuleDebugUi import Ui_ModuleDebug
from device import Device
from time import time

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
        self.log = None

        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.read_inputs)

        self.data1 = 100*[0.0]
        self.data2 = 100*[0.0]

    @pyqtSlot(int)
    def on_dialPWM1_valueChanged(self, val):
        self.dev.pwm(1, val)

    @pyqtSlot(int)
    def on_dialPWM2_valueChanged(self, val):
        self.dev.pwm(2, val)

    @pyqtSlot(int)
    def on_dialAMP1_valueChanged(self, val):
        self.dev.opamp(1, val)

    @pyqtSlot(int)
    def on_dialAMP2_valueChanged(self, val):
        self.dev.opamp(2, val)

    @pyqtSlot(bool)
    def on_radioSine_clicked(self, checked):
        self.dev.ddswave(0)

    @pyqtSlot(bool)
    def on_radioSquare_clicked(self, checked):
        self.dev.ddswave(1)

    @pyqtSlot(bool)
    def on_radioSaw_clicked(self, checked):
        self.dev.ddswave(2)

    @pyqtSlot(bool)
    def on_radioInvSaw_clicked(self, checked):
        self.dev.ddswave(3)

    @pyqtSlot(int)
    def on_dialDDS_valueChanged(self, val):
        self.dev.ddsfreq(val)

    @pyqtSlot()
    def on_comboAMP1_changed(self):
        c = self.ui.comboAMP1c.currentIndex()
        g = self.ui.comboAMP1g.currentIndex()
        self.dev.opamp(1, c, g)

    @pyqtSlot()
    def on_comboAMP2_changed(self):
        c = self.ui.comboAMP2c.currentIndex()
        g = self.ui.comboAMP2g.currentIndex()
        self.dev.opamp(2, c, g)

    @pyqtSlot()
    def on_switches_changed(self):
        s = (self.ui.pushSwitch1.isChecked() and 1 or 0,
             self.ui.pushSwitch2.isChecked() and 1 or 0,
             self.ui.pushSwitch3.isChecked() and 1 or 0,
             self.ui.pushSwitch4.isChecked() and 1 or 0,
             self.ui.pushSwitch5.isChecked() and 1 or 0,
             self.ui.pushSwitch6.isChecked() and 1 or 0)
        self.dev.switches(s[0] + (s[1]<<1) + (s[2]<<2) + (s[3]<<3) + (s[4]<<4) + (s[5]<<5))

    @pyqtSlot()
    def on_pins_changed(self):
        s = (self.ui.pushPin1.isChecked() and 1 or 0,
             self.ui.pushPin2.isChecked() and 1 or 0,
             self.ui.pushPin3.isChecked() and 1 or 0)
        self.ui.pushOut1.setEnabled(not s[0])
        self.ui.pushOut2.setEnabled(not s[1])
        self.ui.pushOut3.setEnabled(not s[2])
        self.dev.setpins(s[0] + (s[1]<<1) + (s[2]<<2))

    @pyqtSlot(bool)
    def on_pushOut1_clicked(self, checked):
        self.dev.setout(1, checked and 1 or 0)

    @pyqtSlot(bool)
    def on_pushOut2_clicked(self, checked):
        self.dev.setout(2, checked and 1 or 0)

    @pyqtSlot(bool)
    def on_pushOut3_clicked(self, checked):
        self.dev.setout(3, checked and 1 or 0)

    @pyqtSlot(int)
    def on_dialInputFreq_valueChanged(self, val):
        self.timer.stop()
        self.ui.pushLog.setEnabled(val > 0)
        if val > 0:
            self.timer.start(1000.0/val)
        else:
            self.ui.labelAD0.setText('AD0: -')
            self.ui.labelAD1.setText('AD1: -')
            self.ui.labelAD2.setText('AD2: -')
            self.ui.labelAD3.setText('AD3: -')
            self.ui.labelAD4.setText('AD4: -')
            self.ui.labelAD5.setText('AD5: -')
            self.ui.labelAD6.setText('AD6: -')
            self.ui.labelIO1.setText('IO1: -')
            self.ui.labelIO2.setText('IO2: -')
            self.ui.labelIO3.setText('IO3: -')

    @pyqtSlot(bool)
    def on_pushLog_clicked(self, checked):
        if checked:
            self.log = open('edubrm.log', 'w')
        else:
            self.log.close()
            self.log = None

    def read_inputs(self):
        r = self.dev.read()
        if self.log:
            self.log.write('%0.6f;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d\n' % (time(), r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]))
        self.ui.labelAD0.setText('AD0: ' + str(r[0]))
        self.ui.labelAD1.setText('AD1: ' + str(r[1]))
        self.ui.labelAD2.setText('AD2: ' + str(r[2]))
        self.ui.labelAD3.setText('AD3: ' + str(r[3]))
        self.ui.labelAD4.setText('AD4: ' + str(r[4]))
        self.ui.labelAD5.setText('AD5: ' + str(r[5]))
        self.ui.labelAD6.setText('AD6: ' + str(r[6]))
        self.ui.labelIO1.setText('IO1: ' + str(r[7]))
        self.ui.labelIO2.setText('IO2: ' + str(r[8]))
        self.ui.labelIO3.setText('IO3: ' + str(r[9]))
        v1 = -1
        if self.ui.comboChart1.currentIndex() > 0:
            v1 = r[self.ui.comboChart1.currentIndex() - 1]
        v2 = -1
        if self.ui.comboChart2.currentIndex() > 0:
            v2 = r[self.ui.comboChart2.currentIndex() - 1]
        if v1 != -1 or v2 != -1:
            self.chart(v1, v2)

    def setup_scene(self, scene):
        scene.addLine(-5, 0, 205, 0)
        scene.addLine(-5, -512/6, 205, -512/6)
        scene.addLine(-5, -1023/6, 205, -1023/6)
        scene.addSimpleText('0').moveBy(-40, -10)
        scene.addSimpleText('512').moveBy(-40, -512/6-10)
        scene.addSimpleText('1023').moveBy(-40, -1023/6-10)

    def chart(self, v1, v2):
        self.data1.pop(0)
        self.data2.pop(0)
        self.data1.append(v1)
        self.data2.append(v2)
        self.scene1 = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        self.setup_scene(self.scene1)
        self.setup_scene(self.scene2)
        path = QPainterPath()
        path.moveTo(0,-self.data1[0]/6)
        for i in xrange(1,100):
            path.lineTo(2*(i+1), -self.data1[i]/6)
        self.scene1.addPath(path, QPen(QColor(0,0,255), 3))
        path = QPainterPath()
        path.moveTo(0,-self.data2[0]/6)
        for i in xrange(1,100):
            path.lineTo(2*(i+1), -self.data2[i]/6)
        self.scene2.addPath(path, QPen(QColor(0,0,255), 3))
        self.ui.chart1.setScene(self.scene1)
        self.ui.chart2.setScene(self.scene2)

class ModuleDebug():

    def __init__(self):
        self.title = 'Debug'
        self.widget = ModuleDebugWidget()

    def start(self):
        self.widget.dev = Device()

    def stop(self):
        self.widget.timer.stop()
