import matplotlib
import numpy

from dichalcogenides.dichalcogenide import Optical, UpperValenceBand
from dichalcogenides.superconductor import Induced

from . import Plot

def main():
    plot_optical('mose2', 'ws2', 'wse2')

def plot_optical(*materials):
    plot = PlotOptical(None, 'induced')

    legend = []
    for material in materials:
        plot.material = material
        legend.append(plot.dichalcogenide.material.name)
        plot.plot_all()

    legend = ['$\\mathregular{' + l + '}$' for l in legend]
    plot.plot[0].legend(legend)
    plot.save()

class PlotOptical(Plot):
    def __init__(self, material, system):
        self.material = material
        self.system = system
        self.opts = dict(
            n=100 # linspace points
        )
        super(self.__class__, self).__init__('optical-transitions')

    @property
    def plot(self):
        """Create and configure the plot object."""
        if not hasattr(self, '_plot'):
            matplotlib.rcParams.update({'font.size': 12})
            self._plot = [
                self.figure.add_subplot(211),
                self.figure.add_subplot(212)
            ]
            self.plot[0].axes.get_xaxis().set_visible(False)
            self.plot[1].set_xlabel('$\\lambda_{\\mathbf{k}} / \\Delta_0$')
            units = ' ($\\mathregular{GeV}$)'
            self.plot[0].set_ylabel('$\\left|P_+\\right|$' + units)
            self.plot[1].set_ylabel('$\\left|P_-\\right|$' + units)
            self.figure.subplots_adjust(hspace=0.1)
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
        sc_trig = sc.trig('sin^2 β')

        p = Optical(self.dichalcogenide).p_circular
        psc = lambda a, lk: sc_trig(dk, lk) * p(xi(dk, lk) + uvb.μ, 1, a)
        fn_m = lambda lk: numpy.sqrt(psc(-1, lk))
        fn_p = lambda lk: numpy.sqrt(psc(1, lk))

        lk = numpy.linspace(*sc.λk_bounds(dk), self.opts['n'])
        x = lk / dk

        err = numpy.geterr()
        numpy.seterr(invalid='ignore')

        line = next(self.lines)
        self.plot[0].plot(
            x, numpy.vectorize(fn_p)(x * dk),
            line, color='black', linewidth=2)

        self.plot[1].plot(
            x, numpy.vectorize(fn_m)(x * dk),
            line, color='black', linewidth=2)

        numpy.seterr(**err)

        return self
