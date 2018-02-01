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
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.treatmentArea('BOD'))
    print("The Kadlec Submerged Bed Area (m^2):", KadlecSSF.safeFunctionCall("area", 'BOD'))

    CEFONMA.necessaryEffluentQuality['BOD'] = 30
    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.treatmentArea('BOD'))
    print("The Kadlec Submerged Bed Area (m^2):", KadlecSSF.safeFunctionCall("area", 'BOD'))
    
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    CEFONMA.necessaryEffluentQuality['TSS'] = 15

    CEFONMA.area= 300
    print("Based on an effluent area value of", CEFONMA.necessaryEffluentQuality['TSS'])
    print("The Reed Submerged TSS Effluent:", ReedSSF.effluent('TSS'))
    print("The Kadlec Submerged Bed TSS Effluent:", KadlecSSF.safeFunctionCall("effluent", 'TSS'))

    CEFONMA.area = 1000
    print("Based on an effluent area value of", CEFONMA.necessaryEffluentQuality['TSS'])
    print("The Reed Submerged Bed TSS Effluent:", ReedSSF.effluent('TSS'))
    print("The Kadlec Submerged Bed TSS Effluent:", KadlecSSF.safeFunctionCall("effluent", 'TSS'))

    

    output.printAreaGraph(ReedSSF, 'BOD', 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', 10, 800, [155, 286])
    output.printAreaGraph(KadlecSSF, 'BOD', 15, 800, [155, 286])
    
 
    
    
    output.printMultipleModelsArea(KadlecSSF, 10, 800, [])
    output.printMultipleModelsArea(ReedSSF, 10, 800, [])

    ReedSSF.printMediaCharacteristicsTable()
    output.printTable21_1(KadlecSSF)
    
    CEFONMA.__init__()
    output.printTableOfEffluent(KadlecSSF, [500, 1000, 10000])
    KadlecSSF.effluent('fecalColiform')
        

if __name__ == '__main__': main()
