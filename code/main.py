"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow
from present import PresentData

def main():

    CEFONMA = Site()    
    ReedSSF = ReedSubsurfaceFlow()
    ReedFWF = ReedFreewaterFlow()
    KadlecSSF = KadlecSubsurfaceFlow(CEFONMA)
    output = PresentData()
    
    #Examples of graphs being printed

    output.printAreaGraph(ReedSSF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(KadlecSSF, 'BOD', CEFONMA, 15, 800, [155, 286])
    
 
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    CEFONMA.necessaryEffluentQuality['TSS'] = 15
    
    output.printMultipleModelsArea(KadlecSSF, CEFONMA, 10, 800, [])
    output.printMultipleModelsArea(ReedSSF, CEFONMA, 10, 800, [])

    ReedSSF.printMediaCharacteristicsTable()
           

if __name__ == '__main__': main()
