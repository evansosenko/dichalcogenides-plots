import numpy

from dichalcogenides.dichalcogenide import Optical, UpperValenceBand
from dichalcogenides.superconductor import Induced

from . import Plot

def main():
    plot_optical('mos2', 'mose2', 'ws2', 'wse2')

def plot_optical(*materials):
    plot = PlotOptical(None, 'induced')

    legend = []
    for material in materials:
        plot.material = material
        legend.append(plot.dichalcogenide.material.name)
        plot.plot_all()

    legend = ['$\\mathregular{' + l + '}$' for l in legend]
    plot.plot.legend(legend)
    plot.save()

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
            self.plot.set_xlabel('$\\lambda_{\\mathbf{k}}$ (eV)')
            self.plot.set_ylabel('$\\frac{P_+^2 - P_-^2}{P_+^2 + P_-^2}$')
        return self._plot

    def plot_all(self):
        """Create complete figure."""
        self.plot_sc_p()
        return self

    def plot_sc_p(self):
        uvb = UpperValenceBand(self.dichalcogenide)
        sc = Induced(self.dichalcogenide)
        xi = sc.ξ
        dk = sc.Δk(0)
        sin2 = sc.trig('sin^2 β')

        p = lambda a: Optical(self.dichalcogenide, 1, a).p_circular
        psc = lambda a, lk: sin2(dk, lk) * p(a)(xi(dk, lk) + uvb.μ)
        fn = lambda lk: (psc(1, lk) - psc(-1, lk)) / (psc(1, lk) + psc(-1, lk))

        lk = numpy.linspace(*sc.λk_bounds(dk), self.opts['n'])

        err = numpy.geterr()
        numpy.seterr(invalid='ignore')
        self.plot.plot(lk, numpy.vectorize(fn)(lk))
        numpy.seterr(**err)

        return self

    def plot_rate(self, alpha):
        uvb = UpperValenceBand(self.dichalcogenide)
        p = Optical(self.dichalcogenide, 1, alpha).p_circular
        xi = numpy.linspace(*uvb.ξ_bounds, self.opts['n'])

        fn = lambda xi: p(xi + uvb.μ)
        self.plot.plot(
            xi, numpy.vectorize(fn)(xi))

        return self

    def plot_p(self):
        uvb = UpperValenceBand(self.dichalcogenide)
        p = lambda a: Optical(self.dichalcogenide, 1, a).p_circular
        xi = numpy.linspace(*uvb.ξ_bounds, self.opts['n'])

        pxi = lambda a, xi: p(a)(xi + uvb.μ)
        fn = lambda xi: (pxi(1, xi) - pxi(-1, xi)) / (pxi(1, xi) + pxi(-1, xi))

        self.plot.plot(
            xi, numpy.vectorize(fn)(xi))

        return self

    def plot_sc_rate(self, alpha):
        uvb = UpperValenceBand(self.dichalcogenide)
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
