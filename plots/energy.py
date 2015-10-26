import itertools

import numpy
from dichalcogenides.dichalcogenide import Energy, UVBEnergy, Dichalcogenide

from . import Plot

def main():
    PlotBands('wse2').plot_all().save()

class PlotBands(Plot):
    """Plot dichalcogenide band structure."""
    def __init__(self, material):
        self.material = material
        super(self.__class__, self).__init__('bands')

        # Global layout parameters.
        self.dk = 0.4 # valley width
        self.k0 = 0.5 # valley separation
        self.t = 0.06 # text offset
        self.tr = 0.01 # relative text offset

    @property
    def plot(self):
        """Create and configure the plot object."""
        if not hasattr(self, '_plot'):
            self._plot = self.figure.add_subplot(111)
            self.plot.axis('off')
        return self._plot

    @property
    def figure_args(self):
        if not hasattr(self, '_figure_args'):
            self._figure_args = {}
        return self._figure_args

    def plot_all(self):
        self.plot_bands()
        self.plot_axes()
        self.plot_chemical_potential()
        self.plot_dimensions()
        self.plot_labels()
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
        e = Energy(self.dichalcogenide).e
        k0, dk, t = self.k0, self.dk, self.t

        p = (-1, 1)
        for x in itertools.product(p, p, p):
            k = numpy.linspace(x[1] * (k0 - dk), x[1] * (k0 + dk), 100)
            fn = lambda k: e(k - x[1] * k0, *x)

            # Plot band.
            self.plot.plot(
                k, numpy.vectorize(fn)(k),
                color='black')

            # Add spin annotation.
            valign = ['bottom', 'top']
            if x[0] == -1: valign.reverse()
            valign.insert(0, None)
            self.plot.annotate(self.spin(
                x[2]), (x[1] * (k0 + dk + t), fn(x[1] * (k0 + dk))),
                horizontalalignment='center',
                verticalalignment=valign[x[0] * x[1] * x[2]])

        return self

    def plot_dimensions(self):
        """Add band gap and spin splitting dimensions."""
        uvb = UVBEnergy(self.dichalcogenide)
        e = Energy(self.dichalcogenide).e
        k0, t, tr = self.k0, self.t, self.tr

        dimension_style = dict(
            arrowstyle='|-|',
            linewidth=0.5,
            mutation_scale=5)

        self.plot.annotate(
            '', (-k0, e(0, -1, 1, 1)), (-k0, e(0, 1, 1, 1)),
           arrowprops=dimension_style)

        self.plot.annotate(
            '$\\Delta$', (0.22, 0.5 + tr), xycoords='axes fraction')

        self.plot.annotate(
            '', (-k0, e(0, -1, 1, 1)), (-k0, e(0, -1, 1, -1)),
            arrowprops=dimension_style)

        self.plot.annotate(
            '$2 \\lambda$', (-k0 - t, uvb.μ + t))

        return self

    def plot_labels(self):
        tr = self.tr

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

        return self


    def plot_chemical_potential(self):
        """Add chemical potential."""
        uvb = UVBEnergy(self.dichalcogenide)
        self.plot.axhline(uvb.μ, linestyle='--', color='black')
        self.plot.annotate('$\\mu$', (-1.5 * self.k0, uvb.μ + self.t))

        return self

    @staticmethod
    def spin(s):
        return [None, '$\\uparrow$', '$\\downarrow$'][s]
