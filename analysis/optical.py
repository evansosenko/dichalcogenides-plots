import os

import matplotlib.pyplot
import numpy

from dichalcogenides.dichalcogenide import Energy, Optical, Dichalcogenide
from dichalcogenides.superconductor import Induced

DATA = 'data'

def main():
    op('mos2')

def save(figure, name):
    if not os.path.isdir('build'): os.makedirs('build')
    path = os.path.join('build', name)
    figure.savefig(path + '.svg')
    figure.savefig(path + '.pdf', format='pdf')

def new_figure():
    return matplotlib.pyplot.figure()

def data_root():
    return os.environ['DATA'] if 'DATA' in os.environ else DATA

def op(material):
    fig = new_figure()
    n = 50

    dichalcogenide = Dichalcogenide(material, 'induced', data_root())
    energy = Energy(dichalcogenide)
    mu = energy.μ
    sc = Induced(dichalcogenide)
    trig = sc.trig

    def coff(xi):
        if xi > 0:
            return trig('cos^2 β')(xi + mu)
        elif xi < 0:
            return trig('sin^2 β')(xi + mu)
        else:
            return 0

    func = lambda xi: coff(xi) * optical.p_circular(xi + mu)

    plot = fig.add_subplot(111)
    x = numpy.linspace(*energy.ξ_bounds + (n,))

    for v in [1, -1]:
        optical = Optical(dichalcogenide, 1, v)
        eq = numpy.vectorize(func)
        plot.plot(x, eq(x))

    save(fig, 'optical')
