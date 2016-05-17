import itertools

import matplotlib
import numpy

from dichalcogenides.dichalcogenide import Energy, UpperValenceBand

from . import Plot

def main():
    """Create and save all plots."""
    PlotBands('wse2').plot_all().save()

class PlotBands(Plot):
    """Plot dichalcogenide band structure."""

    def __init__(self, material):
        self.material = material
        self.opts = dict(
            dk=0.4, # valley width
            k0=0.5, # valley separation
            t=0.06, # text offset
            tr=0.01, # relative text offset
            n=100 # linspace points
        )
        super(self.__class__, self).__init__('energy-bands')

    @property
    def plot(self):
        """Create and configure the plot object."""
        if not hasattr(self, '_plot'):
            matplotlib.rcParams.update({'font.size': 22})
            self._plot = self.figure.add_subplot(111)
            self.plot.axis('off')
        return self._plot

    def plot_all(self):
        """Create complete figure."""
        (self.plot_bands()
         .plot_chemical_potential()
         .plot_axes()
         .plot_dimensions()
         .plot_labels()
         .plot_spins())
        return self

    def plot_axes(self):
        """Create and label center axes."""
        axes_style = dict(
            linewidth=0.5,
            color='gray')

        self.plot.axhline(**axes_style)
        self.plot.axvline(**axes_style)
        self.plot.annotate(
            '$E(k)$', (0.5, 1.05),
             xycoords='axes fraction',
             horizontalalignment='center',
             verticalalignment='center')

        return self

    def plot_bands(self):
        """Plot energy bands."""
        e = Energy(self.dichalcogenide).e
        k0, dk = self.opts['k0'], self.opts['dk']

        p = (-1, 1)
        for x in itertools.product(p, p, p):
            k = numpy.linspace(x[1] * (k0 - dk), x[1] * (k0 + dk), self.opts['n'])
            fn = lambda k: e(k - x[1] * k0, *x)
            self.plot.plot(
                k, numpy.vectorize(fn)(k),
                color='black')

        return self

    def plot_chemical_potential(self):
        """Add chemical potential."""
        k0, t = self.opts['k0'], self.opts['t']
        uvb = UpperValenceBand(self.dichalcogenide)
        self.plot.axhline(uvb.μ, linestyle='--', color='black')
        self.plot.annotate('$\\mu$', (-1, uvb.μ + t))

        return self

    def plot_dimensions(self):
        """Add band gap and spin splitting dimensions."""
        e = Energy(self.dichalcogenide).e
        k0, t, tr = self.opts['k0'], self.opts['t'], self.opts['tr']

        dimension_style = dict(
            arrowstyle='|-|',
            linewidth=0.5,
            mutation_scale=5)

        self.plot.annotate(
            '', (-k0, e(0, -1, 1, 1)), (-k0, e(0, 1, 1, 1)),
           arrowprops=dimension_style)

        self.plot.annotate(
            '$\\Delta$', (-k0 + 0.5 * t, 0 + t))

        self.plot.annotate(
            '', (-k0, e(0, -1, 1, 1)), (-k0, e(0, -1, 1, -1)),
            arrowprops=dimension_style)

        self.plot.annotate(
            '$2 \\lambda$',
            (-k0 + 0.5 * t, 0.5 * (e(0, -1, 1, 1) + e(0, -1, 1, -1)) - 3.5 * t))

        return self

    def plot_labels(self):
        """Add band and valley annotations."""
        tr = self.opts['tr']

        # Add valley labels.
        self.plot.annotate('$\\tau = -$', (0, 0.5 + tr), xycoords='axes fraction')
        self.plot.annotate('$\\tau = +$', (1, 0.5 + tr), xycoords='axes fraction',
                           horizontalalignment='right')

        # Add band labels.
        self.plot.annotate(
            '$n = -$', (0.5 + tr, 0.5 - tr), xycoords='axes fraction',
            verticalalignment='top',
            horizontalalignment='left')

        self.plot.annotate(
             '$n = +$', (0.5 + tr, 0.5 + tr), xycoords='axes fraction',
             verticalalignment='bottom',
             horizontalalignment='left')

        # Add valley momentum labels.
        self.plot.annotate(
            '$\\mathbf{K}$', (0.75, 0.1 - tr), xycoords='axes fraction',
            verticalalignment='top',
            horizontalalignment='center')

        self.plot.annotate(
            '$- \\mathbf{K}$', (0.25, 0.1 - tr), xycoords='axes fraction',
            verticalalignment='top',
            horizontalalignment='center')

        return self

    def plot_spins(self):
        """Add spin annotation."""
        e = Energy(self.dichalcogenide).e
        k0, dk, t = self.opts['k0'], self.opts['dk'], self.opts['t']

        p = (-1, 1)
        for x in itertools.product(p, p, p):
            fn = lambda k: e(k - x[1] * k0, *x)
            valign = ['bottom', 'top']
            if x[0] == -1: valign.reverse()
            valign.insert(0, None)
            self.plot.annotate(self.spin(
                x[2]), (x[1] * (k0 + dk + t), fn(x[1] * (k0 + dk))),
                horizontalalignment='center',
                verticalalignment=valign[x[0] * x[1] * x[2]])

        return self

    @staticmethod
    def spin(s):
        """Map plus and minus one to TeX spin arrow."""
        return [None, '$\\uparrow$', '$\\downarrow$'][s]
