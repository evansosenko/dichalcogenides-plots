import numpy

from dichalcogenides.dichalcogenide import Optical, UVBEnergy

from . import Plot

def main():
    PlotOptical('wse2').plot_all().save()

class PlotOptical(Plot):
    def __init__(self, material):
        self.material = material
        self.opts = dict(
            n=100 # linspace points
        )
        super(self.__class__, self).__init__('optical')

    @property
    def plot(self):
        """Create and configure the plot object."""
        if not hasattr(self, '_plot'):
            self._plot = self.figure.add_subplot(111)
        return self._plot

    def plot_all(self):
        """Create complete figure."""
        self.plot_rate(1).plot_rate(-1)
        return self

    def plot_rate(self, alpha):
        uvb = UVBEnergy(self.dichalcogenide)
        p = Optical(self.dichalcogenide, 1, alpha).p_circular
        xi = numpy.linspace(*uvb.ξ_bounds, self.opts['n'])

        fn = lambda xi: p(xi + uvb.μ)
        self.plot.plot(
            xi, numpy.vectorize(fn)(xi))

        return self
