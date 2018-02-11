"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow, Kadlec2009
from present import PresentData

def main():

    CEFONMA = Site()    
    ReedSSF = ReedSubsurfaceFlow(CEFONMA)
    ReedFWF = ReedFreewaterFlow(CEFONMA)
    KadlecSSF = KadlecSubsurfaceFlow(CEFONMA)
    KadlecPkC = Kadlec2009(CEFONMA)
    output = PresentData(CEFONMA)
    
    #Examples of graphs being printed
    """ 
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.treatmentArea('BOD'))
    print("The k-C* Submerged Bed Area (m^2):", KadlecSSF.safeFunctionCall("area", 'BOD'))
    print("The P-k-C* Submerged Bed Area (m^2):", KadlecPkC.area('BOD', 8))
    """
    
    CEFONMA.necessaryEffluentQuality['BOD'] = 30
    CEFONMA.area = 1000
    CEFONMA.avgFlowRate = 76.65

    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.area('BOD'))
    print("The k-C* Submerged Bed Area (m^2):", KadlecSSF.safeFunctionCall("area", 'BOD'))
    print("The P-k-C* Submerged Bed Area (m^2):", KadlecPkC.area('BOD'))
    print("The P-k-C* BOD effluent for 1000 m^2:", KadlecPkC.effluent('BOD'))


    """
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
    """
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    CEFONMA.necessaryEffluentQuality['TSS'] = 15 

    output.printAreaGraph(ReedSSF, 'BOD', 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', 10, 800, [155, 286])


    output.printAreaGraph(KadlecPkC, 'BOD', 15, 800, [155, 286])
    
 
    
    
    output.printMultipleModelsArea(KadlecSSF, 15, 800, [])
    output.printMultipleModelsArea(ReedSSF, 15, 800, [])
    #output.printMultipleModelsArea(KadlecPkC, 15, 800, [])

    #output.printMediaCharacteristicsTable(ReedSSF)
    output.printTable21_1(KadlecSSF) 
    
    output.printTableOfEffluent(KadlecSSF, [500, 1000, 10000])

    KadlecSSF.effluent('fecalColiform')
    
    output.printTable('annualAndMonthlyTemps', CEFONMA.climateTemps, title='Annual and Monthly Temps')
    output.printTable('mediaCharacteristicsReed', ReedSSF.mediaCharacteristicsTable, title="Typical Media Characteristics for Subsurface Flow Wetlands")
    output.printTable("annualAndMonthlySnowfall", CEFONMA.snowfall, title="Annual and Monthly Snowfall")
    output.printTable("annualAndMonthlyRainfall", CEFONMA.rainfall, title="Annual and Monthly Rainfall")
    output.printTable("annualAndMonthlyEvapo", CEFONMA.evapotranspiration, title="Annual and Monthly Evapotranspiration")
    output.printTable("firstOrderBODRateConstantsKadlec", KadlecPkC.tableBODRateConstants, "Summary of First-Order Rate Constants for Selected Parameters")
    output.printTable("firstOrderRateConstantsKadlec", KadlecPkC.tableRateConstants, "Summary of First-Order Rate Constants for Selected Parameters")


    CEFONMA.avgFlowRate = 20
    CEFONMA.numberOfCells = 4
    CEFONMA.area = 500
    CEFONMA.porosity = 0.38
    CEFONMA.depth = 0.30
    CEFONMA.currentSepticTankEffluent['BOD'] = 200
    CEFONMA.tankArea = 125
    CEFONMA.backgroundEffluent['BOD']
    output.printTable20_1('Table20_1', 'BOD', k=45/365)
        

if __name__ == '__main__': main()
