import numpy

from dichalcogenides.dichalcogenide import UVBEnergy, Energy, Topology
from dichalcogenides.superconductor import Induced

from . import Plot

def main():
    plot_berry_curvature('mos2', 'mose2', 'ws2', 'wse2')

def plot_berry_curvature(*materials):
    plot = PlotBerry(None, 'induced')

    legend = []
    for material in materials:
        plot.material = material
        legend.append(plot.dichalcogenide.material.name)
        plot.plot_all()

    legend = ['$\\mathregular{' + l + '}$' for l in legend]
    plot.plot.legend(legend)
    plot.save()

class PlotBerry(Plot):
    def __init__(self, material, system):
        self.material = material
        self.system = system
        self.opts = dict(
            n=100 # linspace points
        )
        super(self.__class__, self).__init__('topology')

    @property
    def plot(self):
        """Create and configure the plot object."""
        if not hasattr(self, '_plot'):
            self._plot = self.figure.add_subplot(111)
            self.plot.set_xlabel('$\\lambda_{\\mathbf{k}}$ (eV)')
            self.plot.set_ylabel('')
        return self._plot

    def plot_all(self):
        """Create complete figure."""
        self.plot_sc_bc()
        return self

    def plot_sc_bc(self):
        uvb = UVBEnergy(self.dichalcogenide)
        energy = Energy(self.dichalcogenide)
        bc = Topology(self.dichalcogenide).Ω
        sc = Induced(self.dichalcogenide)

        sin2 = sc.trig('sin^2 β')
        xi = sc.ξ
        dk = sc.Δk(0)

        p = (1, 1, 1)
        c = lambda e: bc(energy.k(e, *p), *p)
        fn = lambda lk: sin2(dk, lk)**3 * c(xi(dk, lk) + uvb.μ)

        lk = numpy.linspace(*sc.λk_bounds(dk), self.opts['n'])
        self.plot.plot(lk, numpy.vectorize(fn)(lk))

        return self
