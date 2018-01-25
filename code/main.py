"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow, PresentData

def main():

    CEFONMA = Site()    
    ReedSSF = ReedSubsurfaceFlow()
    ReedFWF = ReedFreewaterFlow()
    KadlecSSF = KadlecSubsurfaceFlow()
    output = PresentData()
    
    #print("Kadlec Area needed (with BOD = 155): %d m^2" % Reed.treatmentArea('BOD', CEFONMA))

    output.printAreaGraph(ReedSSF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(KadlecSSF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printMultipleModels([ReedSSF, KadlecSSF], 'BOD', CEFONMA, 10, 800, [155, 286])
           



if __name__ == '__main__': main()
