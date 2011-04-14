from module import Module
from ModuleDebugUi import Ui_ModuleDebug

class ModuleDebug(Module):

    title = 'Debug'

    def setup(self, area):
        print 'setup Debug'
        self.ui = Ui_ModuleDebug()
        self.ui.setupUi(area)

    def run(self):
        print 'run Debug'
