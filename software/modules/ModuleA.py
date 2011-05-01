from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QPainterPath
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QColor
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QTimer
from ModuleAUi import Ui_ModuleA
from device import Device

class ModuleAWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ModuleA()
        self.ui.setupUi(self)

        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"), self.read_inputs)

        self.scene = QGraphicsScene()
        self.ui.graphU.setScene(self.scene)

        self.data = 100*[0.0]

    def read_inputs(self):
        r = self.dev.read()
        u = r[1]/1023.0 * 3.3
        self.ui.labelU.setText('%0.3f V' % u)
        self.ui.progressU.setValue(1000*u)
        self.data.pop(0)
        self.data.append(u)

        self.scene = QGraphicsScene()
        self.scene.addLine(-10, 400-0, 610, 400-0)
        self.scene.addLine(0, 400+10, 0, 400-410)
        self.scene.addLine(-10, 400- 50, 10, 400- 50)
        self.scene.addLine(-10, 400-100, 10, 400-100)
        self.scene.addLine(-10, 400-150, 10, 400-150)
        self.scene.addLine(-10, 400-200, 10, 400-200)
        self.scene.addLine(-10, 400-250, 10, 400-250)
        self.scene.addLine(-10, 400-300, 10, 400-300)
        self.scene.addLine(-10, 400-350, 10, 400-350)
        self.scene.addLine(-10, 400-400, 10, 400-400)
        self.scene.addSimpleText('4.0').moveBy(-40,   0-10)
        self.scene.addSimpleText('3.5').moveBy(-40,  50-10)
        self.scene.addSimpleText('3.0').moveBy(-40, 100-10)
        self.scene.addSimpleText('2.5').moveBy(-40, 150-10)
        self.scene.addSimpleText('2.0').moveBy(-40, 200-10)
        self.scene.addSimpleText('1.5').moveBy(-40, 250-10)
        self.scene.addSimpleText('1.0').moveBy(-40, 300-10)
        self.scene.addSimpleText('0.5').moveBy(-40, 350-10)
        self.scene.addSimpleText('0.0').moveBy(-40, 400-10)
        self.scene.addSimpleText('[U]').moveBy(-39, 430-10)
        path = QPainterPath()
        path.moveTo(0,400-self.data[0]*100)
        for i in xrange(1,100):
            path.lineTo(6*(i+1), 400-self.data[i]*100)
        self.scene.addPath(path, QPen(QColor(0,0,255), 3))
        self.ui.graphU.setScene(self.scene)

class ModuleA():

    def __init__(self):
        self.title = 'Sources of Electricity'
        self.widget = ModuleAWidget()

    def start(self):
        self.widget.dev = Device()
        self.widget.timer.start(50)

    def stop(self):
        self.widget.timer.stop()
