from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QPainterPath
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QColor
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

        self.data1 = 200*[0.0]
        self.data2 = 200*[0.0]

        self.mode = ['DC', 'L']

    @pyqtSlot()
    def on_radioAC_clicked(self):
        self.mode[0] = 'AC'
        self.setup_hw()

    @pyqtSlot()
    def on_radioDC_clicked(self):
        self.mode[0] = 'DC'
        self.setup_hw()

    @pyqtSlot()
    def on_radioL_clicked(self):
        self.mode[1] = 'L'
        self.setup_hw()

    @pyqtSlot()
    def on_radioC_clicked(self):
        self.mode[1] = 'C'
        self.setup_hw()

    @pyqtSlot()
    def on_radioLC_clicked(self):
        self.mode[1] = 'LC'
        self.setup_hw()

    @pyqtSlot()
    def on_btnStart_clicked(self):
        self.ui.btnStart.setEnabled(False)
        self.ui.btnStop.setEnabled(True)
        if self.mode == ['DC', 'L']:
            self.dev.setout(1, 1)
        if self.mode == ['DC', 'C']:
            self.dev.setout(2, 1)
        if self.mode == ['DC', 'LC']:
            self.dev.setout(3, 1)

    @pyqtSlot()
    def on_btnStop_clicked(self):
        self.ui.btnStart.setEnabled(True)
        self.ui.btnStop.setEnabled(False)
        if self.mode == ['DC', 'L']:
            self.dev.setout(1, 0)
        if self.mode == ['DC', 'C']:
            self.dev.setout(2, 0)
        if self.mode == ['DC', 'LC']:
            self.dev.setout(3, 0)

    def setup_hw(self):
        if self.mode == ['DC', 'L']:
            self.dev.switches(1<<0)
        if self.mode == ['DC', 'C']:
            self.dev.switches(1<<1)
        if self.mode == ['DC', 'LC']:
            self.dev.switches(1<<2)

    def setup_scene(self, scene):
        scene.addLine(-5, 200-0, 610, 200-0)
        scene.addLine(0, 200+5, 0, 200-205)
        scene.addLine(-5, 200- 50, 10, 200- 50)
        scene.addLine(-5, 200-100, 10, 200-100)
        scene.addLine(-5, 200-150, 10, 200-150)
        scene.addSimpleText('4.0').moveBy(-40,   0-10)
        scene.addSimpleText('3.0').moveBy(-40,  50-10)
        scene.addSimpleText('2.0').moveBy(-40, 100-10)
        scene.addSimpleText('1.0').moveBy(-40, 150-10)
        scene.addSimpleText('0.0').moveBy(-40, 200-10)

    def tick_DC(self, u, i):
        self.data1.pop(0)
        self.data2.pop(0)
        self.data1.append(u)
        self.data2.append(i)
        self.scene1 = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        self.setup_scene(self.scene1)
        self.setup_scene(self.scene2)
        self.scene1.addSimpleText('[U]').moveBy(-39, 220-10)
        self.scene2.addSimpleText('[I]').moveBy(-39, 220-10)
        path = QPainterPath()
        path.moveTo(0,200-self.data1[0]*50)
        for i in xrange(1,200):
            path.lineTo(3*(i+1), 200-self.data1[i]*50)
        self.scene1.addPath(path, QPen(QColor(0,0,255), 3))
        path = QPainterPath()
        path.moveTo(0,200-self.data2[0]*50)
        for i in xrange(1,200):
            path.lineTo(3*(i+1), 200-self.data2[i]*50)
        self.scene2.addPath(path, QPen(QColor(0,0,255), 3))
        self.ui.graph1.setScene(self.scene1)
        self.ui.graph2.setScene(self.scene2)

    def read_inputs(self):
        r = self.dev.read()

        if self.mode[0] == 'DC':
            u = r[0]/1023.0 * 3.3 # TODO: change this if we change opamp
            i = 1                 # TODO: read real current
            self.tick_DC(u, i)

class ModuleC():

    def __init__(self):
        self.title = 'L/C/LC circuit'
        self.widget = ModuleCWidget()

    def start(self):
        self.widget.dev = Device()
        self.widget.setup_hw()
        self.widget.timer.start(25)

    def stop(self):
        self.widget.timer.stop()
