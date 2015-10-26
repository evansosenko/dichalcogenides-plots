import numpy

from dichalcogenides.dichalcogenide import Optical, UVBEnergy
from dichalcogenides.superconductor import Induced

from . import Plot

def main():
    PlotOptical('wse2', 'induced').plot_all().save()

class PlotOptical(Plot):
    def __init__(self, material, system):
        self.material = material
        self.system = system
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
        self.plot_sc_p()
        return self

    def plot_rate(self, alpha):
        uvb = UVBEnergy(self.dichalcogenide)
        p = Optical(self.dichalcogenide, 1, alpha).p_circular
        xi = numpy.linspace(*uvb.ξ_bounds, self.opts['n'])

        fn = lambda xi: p(xi + uvb.μ)
        self.plot.plot(
            xi, numpy.vectorize(fn)(xi))

        return self

    def plot_p(self):
        uvb = UVBEnergy(self.dichalcogenide)
        p = lambda a: Optical(self.dichalcogenide, 1, a).p_circular
        xi = numpy.linspace(*uvb.ξ_bounds, self.opts['n'])

        pxi = lambda a, xi: p(a)(xi + uvb.μ)
        fn = lambda xi: (pxi(1, xi) - pxi(-1, xi)) / (pxi(1, xi) + pxi(-1, xi))

        self.plot.plot(
            xi, numpy.vectorize(fn)(xi))

        return self

    def plot_sc_rate(self, alpha):
        uvb = UVBEnergy(self.dichalcogenide)
        p = Optical(self.dichalcogenide, 1, alpha).p_circular
        sc = Induced(self.dichalcogenide)
        xi = sc.ξ
        dk = sc.Δk(0)
        s = sc.trig('sin^2 β')

        lk = numpy.linspace(*sc.λk_bounds(dk), self.opts['n'])

        fn = lambda lk: s(dk, lk) * p(xi(dk, lk) + uvb.μ)
        self.plot.plot(
            lk, numpy.vectorize(fn)(lk))

        return self

    def plot_sc_p(self):
        uvb = UVBEnergy(self.dichalcogenide)
        sc = Induced(self.dichalcogenide)
        xi = sc.ξ
        dk = sc.Δk(0)
        s = sc.trig('sin^2 β')

        p = lambda a: Optical(self.dichalcogenide, 1, a).p_circular
        psc = lambda a, lk: s(dk, lk) * p(a)(xi(dk, lk) + uvb.μ)

        fn = lambda lk: (psc(1, lk) - psc(-1, lk)) / (psc(1, lk) + psc(-1, lk))

        lk = numpy.linspace(*sc.λk_bounds(dk), self.opts['n'])

        self.plot.plot(
            lk, numpy.vectorize(fn)(lk))

        return self
