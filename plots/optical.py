import numpy
from dichalcogenides.dichalcogenide import Energy, UVBEnergy, Dichalcogenide

from . import Plot

def main():
    PlotOptical('wse2').save()

class PlotOptical(Plot):
    def __init__(self, material):
        super(self.__class__, self).__init__('optical')

