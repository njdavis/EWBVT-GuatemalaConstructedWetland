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
    KadlecSSF = KadlecSubsurfaceFlow()
    output = PresentData()
    
    #Examples of graphs being printed
    """
    output.printAreaGraph(ReedSSF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(KadlecSSF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printMultipleModelsArea([ReedFWF, ReedSSF, KadlecSSF], 'ammonia', CEFONMA, 10, 800, [])
    """
  
    output.printMultipleModelsEffluent(KadlecSSF, CEFONMA, 10, 800, [])
    output.printMultipleModelsEffluent(ReedSSF, CEFONMA, 10, 800, [])
           



if __name__ == '__main__': main()
