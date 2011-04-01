from module import Module

class ModuleB(Module):

    title = "Bcko"

    def setup(self, area):
        print 'setup B'
        print area
