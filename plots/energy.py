import itertools

import matplotlib
import numpy

from dichalcogenides.dichalcogenide import Energy, UpperValenceBand

from . import Plot

def main():
    """Create and save all plots."""
    PlotBands('wse2').plot_all().save()
    PlotPairs('wse2').plot_all().save()

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
        super(PlotBands, self).__init__('energy-bands')

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
            fn = lambda k, s=x: e(k - s[1] * k0, *s)
            self.plot.plot(
                k, numpy.vectorize(fn)(k),
                color='black')

        return self

    def plot_chemical_potential(self):
        """Add chemical potential."""
        t = self.opts['t']
        uvb = UpperValenceBand(self.dichalcogenide)
        self.plot.axhline(uvb.μ, linestyle='--', color='black')
        self.plot.annotate('$\\mu$', (-1, uvb.μ + t))

        return self

    def plot_dimensions(self):
        """Add band gap and spin splitting dimensions."""
        e = Energy(self.dichalcogenide).e
        k0, t = self.opts['k0'], self.opts['t']

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
            fn = lambda k, s=x: e(k - s[1] * k0, *s)
            valign = ['bottom', 'top']
            if x[0] == -1: valign.reverse()
            valign.insert(0, None)
            self.plot.annotate(
                self.spin(x[2]),
                (x[1] * (k0 + dk + t), fn(x[1] * (k0 + dk))),
                horizontalalignment='center',
                verticalalignment=valign[x[0] * x[1] * x[2]])

        return self

    @staticmethod
    def spin(s):
        """Map plus and minus one to TeX spin arrow."""
        return [None, '$\\uparrow$', '$\\downarrow$'][s]

class PlotPairs(PlotBands):
    """Plot bands with BCS pairing."""

    def __init__(self, material):
        super(PlotPairs, self).__init__(material)
        self.name = 'bcs-pairs'

    def plot_all(self):
        """Create complete figure."""
        (self.plot_bands()
         .plot_chemical_potential()
         .plot_axes()
         .plot_spins()
         .plot_berry()
         .plot_pairs()
         .plot_transition())
        return self

    def plot_berry(self):
        k0, t = self.opts['k0'], self.opts['t']
        self.plot.annotate(
            '$-\\Omega_z$', (-k0, 0 + 25 * t), horizontalalignment='center')
        self.plot.annotate(
            '$+\\Omega_z$', (k0, 0 + 25 * t), horizontalalignment='center')
        return self

    def plot_pairs(self):
        k0 = self.opts['k0']
        e = Energy(self.dichalcogenide).e
        dk = 0.2
        k1 = k0 - dk
        efn = numpy.vectorize(lambda k: e(k, -1, 1, 1))
        self.plot.plot(
            [(k1 - 0.15 * dk), -(k1 - 0.15 * dk)], efn([dk, dk]),
            linestyle='--', linewidth=3, color='black')

        self.plot.plot(
            -k1, efn(dk),
            marker='o', color='black', markersize=10)

        self.plot.plot(
            k1, efn(dk),
            marker='o', color='black', markersize=10, markeredgewidth=2,
            markerfacecolor='none')

        return self

    def plot_transition(self):
        k0, t = self.opts['k0'], self.opts['t']
        e = Energy(self.dichalcogenide).e
        de = 0.1
        dk = 0.2
        k1 = k0 - dk
        self.plot.plot([k1, k1], [e(dk, -1, 1, 1) + de, e(dk, 1, 1, 1) - de],
                       linestyle=':', color='black', linewidth=3)
        self.plot.plot(
            k1, e(dk, 1, 1, 1),
            marker='o', color='black', markersize=10)

        w = 10
        t = numpy.linspace(0.32, 0.6, 1000)
        fn = lambda t: 0.1 * numpy.sin(2 * numpy.pi * w * t)
        self.plot.plot(t, fn(t), color='black', linestyle='-')

        self.plot.annotate(
            '$\\epsilon_+$', (0.83, 0.52),
            xycoords='axes fraction',
            horizontalalignment='center',
            verticalalignment='center')
        return self
