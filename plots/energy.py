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

    def plot_all(self):
        dichalcogenide = Dichalcogenide(self.material, root='data')
        uvb = UVBEnergy(dichalcogenide)
        energy = Energy(dichalcogenide)

        # Define additional parameters.
        e = energy.e
        dk = 0.4 # valley width
        k0 = 0.5 # valley separation
        t = 0.06 # text offset
        tr = 0.01 # relative text offset

        # Set center axes style.
        axes_style = dict(
            linewidth=0.5,
            color='gray')

        # Set dimension annotations style.
        dimension_style = dict(
            arrowstyle='|-|',
            linewidth=0.5,
            mutation_scale=5)

        # Create and configure the plot object.
        plt = self.figure.add_subplot(111)
        plt.axis('off')

        # Add and label center axes.
        plt.axhline(**axes_style)
        plt.axvline(**axes_style)
        plt.annotate('$E(k)$', (0.5, 1.05),
                     xycoords='axes fraction',
                     horizontalalignment='center',
                     verticalalignment='center')

        # Add chemical potential.
        plt.axhline(uvb.μ, linestyle='--', color='black')
        plt.annotate('$\\mu$', (-1.5 * k0, uvb.μ + t))

        # Add band gap dimension.
        plt.annotate('', (-k0, e(0, -1, 1, 1)), (-k0, e(0, 1, 1, 1)),
                     arrowprops=dimension_style)
        plt.annotate('$\\Delta$', (0.22, 0.5 + tr), xycoords='axes fraction')

        # Add spin splitting dimension.
        plt.annotate('', (-k0, e(0, -1, 1, 1)), (-k0, e(0, -1, 1, -1)),
                     arrowprops=dimension_style)
        plt.annotate('$2 \\lambda$', (-k0 - t, uvb.μ + t))

        # Add valley labels.
        plt.annotate('$\\tau = -$', (0, 0.5 + tr), xycoords='axes fraction')
        plt.annotate('$\\tau = +$', (1, 0.5 + tr), xycoords='axes fraction',
                     horizontalalignment='right')

        # Add band labels.
        plt.annotate('$n = -$', (0.5 + tr, 0.5 - tr), xycoords='axes fraction',
                     verticalalignment='top',
                     horizontalalignment='left')
        plt.annotate('$n = +$', (0.5 + tr, 0.5 + tr), xycoords='axes fraction',
                     verticalalignment='bottom',
                     horizontalalignment='left')

        # Add bands.
        p = (-1, 1)
        for x in itertools.product(p, p, p):
            k = numpy.linspace(x[1] * (k0 - dk), x[1] * (k0 + dk), 100)
            fn = lambda k: e(k - x[1] * k0, *x)

            # Plot band.
            plt.plot(
                k, numpy.vectorize(fn)(k),
                color='black')

            # Add spin annotation.
            valign = ['bottom', 'top']
            if x[0] == -1: valign.reverse()
            valign.insert(0, None)
            plt.annotate(self.spin(x[2]), (x[1] * (k0 + dk + t), fn(x[1] * (k0 + dk))),
                     horizontalalignment='center',
                     verticalalignment=valign[x[0] * x[1] * x[2]])

        return self

    @staticmethod
    def spin(s):
        return [None, '$\\uparrow$', '$\\downarrow$'][s]
