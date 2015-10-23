import itertools

import numpy
from dichalcogenides.dichalcogenide import Energy, UVBEnergy, Dichalcogenide

from . import Plot

def main():
    plot_bands('wse2')

def plot_bands(material):
    """Plot dichalcogenide band structure."""
    dichalcogenide = Dichalcogenide(material, root='data')
    uvb = UVBEnergy(dichalcogenide)
    energy = Energy(dichalcogenide)

    # Create and configure plot object.
    plot = Plot('bands')
    plt = plot.figure.add_subplot(111)
    plt.axis('off')

    # Add line for the chemical potential.
    plt.axhline(uvb.μ)

    # Set additional parameters.
    dk = 0.4 # valley width
    k0 = 0.5 # valley separation

    p = (-1, 1)
    for x in itertools.product(p, p, p):
        k = numpy.linspace(x[1] * (-dk + k0), x[1] * (dk + k0), 100)
        plt.plot(k, numpy.vectorize(lambda k: energy.e(k - x[1] * k0, *x))(k))

    plot.save()
