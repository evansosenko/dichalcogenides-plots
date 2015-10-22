import os

import matplotlib.pyplot

class Plot():
    def __init__(self, name, directory='build'):
        self.name = name
        self.directory = directory

    @property
    def path(self):
        return os.path.join(self.directory, self.name)

    @property
    def figure_args(self):
        return {}

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
        print(self.path)
        self.figure.savefig(self.path)
