import os


class Path:
    location = 'helpers/path.py'

    @property
    def root(self):
        return __file__.split(self.location)[0]

    @property
    def routes_root(self):
        return os.path.join(self.root, 'routes/')
