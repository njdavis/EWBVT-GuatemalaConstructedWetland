"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow
from present import PresentData

def main():

    CEFONMA = Site()    
    ReedSSF = ReedSubsurfaceFlow(CEFONMA)
    ReedFWF = ReedFreewaterFlow(CEFONMA)
    KadlecSSF = KadlecSubsurfaceFlow(CEFONMA)
    output = PresentData()
    
    #Examples of graphs being printed
   
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.treatmentArea('BOD', CEFONMA))
    print("The Kadlec Submerged Bed Area (m^2):", KadlecSSF.safeFunctionCall("area", 'BOD', CEFONMA))

    CEFONMA.necessaryEffluentQuality['BOD'] = 30
    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.treatmentArea('BOD', CEFONMA))
    print("The Kadlec Submerged Bed Area (m^2):", KadlecSSF.safeFunctionCall("area", 'BOD', CEFONMA))

    output.printAreaGraph(ReedSSF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', CEFONMA, 10, 800, [155, 286])
    output.printAreaGraph(KadlecSSF, 'BOD', CEFONMA, 15, 800, [155, 286])
    
 
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    CEFONMA.necessaryEffluentQuality['TSS'] = 15
    
    output.printMultipleModelsArea(KadlecSSF, CEFONMA, 10, 800, [])
    output.printMultipleModelsArea(ReedSSF, CEFONMA, 10, 800, [])

    ReedSSF.printMediaCharacteristicsTable()
    KadlecSSF.printTable21_1()
    
    CEFONMA.__init__()
    KadlecSSF.printTableOfEffluent([500, 1000, 10000], CEFONMA)
    KadlecSSF.effluent('fecalColiform', CEFONMA)
        

if __name__ == '__main__': main()
