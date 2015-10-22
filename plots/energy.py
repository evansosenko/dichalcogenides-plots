import itertools

import numpy
from dichalcogenides.dichalcogenide import Energy, Dichalcogenide

from . import Plot

def main():
    plot_bands('mos2')

def plot_bands(material):
    energy = Energy(Dichalcogenide(material, root='data')).e
    plot = Plot('bands')
    plt = plot.figure.add_subplot(111)

    p = (-1, 1)
    for x in itertools.product(p, p, p):
        dk = x[1] * 1
        k0 = x[1] * 1
        k = numpy.linspace(-dk + k0, dk + k0, 100)
        plt.plot(k, numpy.vectorize(lambda k: energy(k - k0, *x))(k))
    plot.save()
