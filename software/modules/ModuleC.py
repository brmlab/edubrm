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

        self.data1 = 100*[0.0]
        self.data2 = 100*[0.0]
        self.data3 = 100*[0.0]
        self.data4 = 100*[0.0]

    def setup_scene(self, scene):
        scene.addLine(-5, 200-0, 260, 200-0)
        scene.addLine(0, 200+5, 0, 200-205)
        scene.addLine(-5, 200- 50, 10, 200- 50)
        scene.addLine(-5, 200-100, 10, 200-100)
        scene.addLine(-5, 200-150, 10, 200-150)
        scene.addSimpleText('4.0').moveBy(-40,   0-10)
        scene.addSimpleText('3.0').moveBy(-40,  50-10)
        scene.addSimpleText('2.0').moveBy(-40, 100-10)
        scene.addSimpleText('1.0').moveBy(-40, 150-10)
        scene.addSimpleText('0.0').moveBy(-40, 200-10)


    def read_inputs(self):
        r = self.dev.read()
        i = r[6]/1023.0 * 3.3
        a = r[0]/1023.0 * 3.3
        b = r[1]/1023.0 * 3.3
        c = r[2]/1023.0 * 3.3

        self.data1.pop(0)
        self.data2.pop(0)
        self.data3.pop(0)
        self.data4.pop(0)
        self.data1.append(i)
        self.data2.append(a)
        self.data3.append(b)
        self.data4.append(c)
        self.scene1 = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        self.scene3 = QGraphicsScene()
        self.scene4 = QGraphicsScene()
        self.setup_scene(self.scene1)
        self.setup_scene(self.scene2)
        self.setup_scene(self.scene3)
        self.setup_scene(self.scene4)

        self.scene1.addSimpleText('[I]').moveBy(-39, 220-10)
        path = QPainterPath()
        path.moveTo(0,200-self.data1[0]*50)
        for i in xrange(1,100):
            path.lineTo(2.5*(i+1), 200-self.data1[i]*50)
        self.scene1.addPath(path, QPen(QColor(0,0,255), 3))

        self.scene2.addSimpleText('[A]').moveBy(-39, 220-10)
        path = QPainterPath()
        path.moveTo(0,200-self.data2[0]*50)
        for i in xrange(1,100):
            path.lineTo(2.5*(i+1), 200-self.data2[i]*50)
        self.scene2.addPath(path, QPen(QColor(0,0,255), 3))

        self.scene3.addSimpleText('[B]').moveBy(-39, 220-10)
        path = QPainterPath()
        path.moveTo(0,200-self.data3[0]*50)
        for i in xrange(1,100):
            path.lineTo(2.5*(i+1), 200-self.data3[i]*50)
        self.scene3.addPath(path, QPen(QColor(0,0,255), 3))

        self.scene4.addSimpleText('[C]').moveBy(-39, 220-10)
        path = QPainterPath()
        path.moveTo(0,200-self.data4[0]*50)
        for i in xrange(1,100):
            path.lineTo(2.5*(i+1), 200-self.data4[i]*50)
        self.scene4.addPath(path, QPen(QColor(0,0,255), 3))

        self.ui.graph1.setScene(self.scene1)
        self.ui.graph2.setScene(self.scene2)
        self.ui.graph3.setScene(self.scene3)
        self.ui.graph4.setScene(self.scene4)

class ModuleC():

    def __init__(self):
        self.title = 'L/C/LC circuit'
        self.widget = ModuleCWidget()

    def start(self):
        self.widget.dev = Device()
        self.widget.timer.start(25)

    def stop(self):
        self.widget.timer.stop()
