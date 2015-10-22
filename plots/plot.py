import os

class Plot():
    def __init__(self, name, directory='build'):
        self.name = name
        self.directory = directory

    @property
    def path(self):
        return os.path.join(self.directory, self.name)
