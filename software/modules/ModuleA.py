from module import Module

class ModuleA(Module):

    title = 'Acko'

    def setup(self, area):
        print 'setup A'

    def run(self):
        print 'run A'
