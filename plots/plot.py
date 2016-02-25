import os
import itertools

import matplotlib.pyplot
from dichalcogenides.dichalcogenide import Dichalcogenide

class Plot():
    def __init__(self, name, directory='build'):
        self.name = name
        self.directory = directory

    @property
    def extensions(self):
        if not hasattr(self, '_extensions'):
            self._extensions = ['eps', 'pdf', 'svg']
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        self._extensions = value

    @property
    def opts(self):
        if not hasattr(self, '_opts'):
            self._opts = {}
        return self._opts

    @opts.setter
    def opts(self, value):
        self._opts = value

    @property
    def material(self):
        if not hasattr(self, '_material'):
            self._material = None
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def system(self):
        if not hasattr(self, '_system'):
            self._system = None
        return self._system

    @system.setter
    def system(self, value):
        self._system = value

    @property
    def lines(self):
        if not hasattr(self, '_lines'):
            self._lines = itertools.cycle(['-','--',':','-.'])
        return self._lines

    @property
    def dichalcogenide(self):
        if not hasattr(self, '_dichalcogenide '):
            self._dichalcogenide = Dichalcogenide(
                self.material, self.system, root='data')
        return self._dichalcogenide

    @property
    def paths(self):
        """Paths to save the figure."""
        return [os.path.join(self.directory, self.name + '.' + extension)
                for extension in self.extensions]

    @property
    def figure_args(self):
        if not hasattr(self, '_figure_args'):
            self._figure_args = {}
        return self._figure_args

    @property
    def figure(self):
        """
        Returns or creates a [`matplotlib.figure.Figure`][1] object.
        Keyword arguments in `figure_args` are passed to [`matplotlib.pyplot.figure`][2].
        [1]: http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
        [2]: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.figure
        """
        if not hasattr(self, '_figure'):
            self._figure = matplotlib.pyplot.figure(**self.figure_args)
        return self._figure

    def close(self):
        """
        Closes the [`matplotlib.figure.Figure`][1] object
        with [`matplotlib.pyplot.close`][2].
        [1]: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.close
        """
        return matplotlib.pyplot.close(self.figure)

    def save(self):
        """Save figure to file."""
        for path in self.paths:
            self.figure.savefig(path, transparent=True)
