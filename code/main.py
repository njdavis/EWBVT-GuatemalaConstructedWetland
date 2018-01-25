"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow

def main():

    CEFONMA = Site()    
    ReedSSF = ReedSubsurfaceFlow()
    ReedFWF = ReedFreewaterFlow()
    Kadlec = KadlecSubsurfaceFlow()
    
    #print("Kadlec Area needed (with BOD = 155): %d m^2" % Reed.treatmentArea('BOD', CEFONMA))

    ReedFWF.printAreaGraph('BOD', CEFONMA, 10, 800, [155, 286])
    ReedSSF.printAreaGraph('BOD', CEFONMA, 10, 800, [155, 286])
    Kadlec.printAreaGraph('BOD', CEFONMA, 10, 800, [155, 286])
           



if __name__ == '__main__': main()
