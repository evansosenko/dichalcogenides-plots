import itertools

import numpy
from dichalcogenides.dichalcogenide import Energy, Dichalcogenide

from . import Plot

def main():
    plot_bands('wse2')

def plot_bands(material):
    energy = Energy(Dichalcogenide(material, root='data')).e
    plot = Plot('bands')
    plt = plot.figure.add_subplot(111)
    plt.axis('off')

    p = (-1, 1)
    for x in itertools.product(p, p, p):
        dk = 0.5
        k0 = 0.5
        s =  0.1
        k = numpy.linspace(x[1] * (-dk + k0 + s), x[1] * (dk + k0 - s), 100)
        plt.plot(k, numpy.vectorize(lambda k: energy(k - x[1] * k0, *x))(k))

    plot.save()
