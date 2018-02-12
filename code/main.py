"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, Kadlec1996SSF, Kadlec2009SSF
from present import PresentData

def main():
    
    CEFONMA = Site()    
    ReedSSF = ReedSubsurfaceFlow(CEFONMA)
    ReedFWF = ReedFreewaterFlow(CEFONMA)
    KadlecSSF_kC = Kadlec1996SSF(CEFONMA)
    KadlecSSF_PkC = Kadlec2009SSF(CEFONMA)
    output = PresentData(CEFONMA)
    
    #Examples of graphs being printed
    """ 
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.treatmentArea('BOD'))
    print("The k-C* Submerged Bed Area (m^2):", KadlecSSF_kC.safeFunctionCall("area", 'BOD'))
    print("The P-k-C* Submerged Bed Area (m^2):", KadlecSSF_PkC.area('BOD', 8))
    """
    
    print("Based on an effluent BOD5 value of", CEFONMA.necessaryEffluentQuality['BOD'])
    print("The Reed Submerged Bed Area (m^2):", ReedSSF.area('BOD'))
    print("The k-C* Submerged Bed Area (m^2):", KadlecSSF_kC.safeFunctionCall("area", 'BOD'))
    print("The P-k-C* Submerged Bed Area (m^2):", KadlecSSF_PkC.area('BOD'))
    print("The P-k-C* BOD effluent for 1000 m^2:", KadlecSSF_PkC.effluent('BOD'))


    """
    CEFONMA.necessaryEffluentQuality['BOD'] = 15
    CEFONMA.necessaryEffluentQuality['TSS'] = 15

    CEFONMA.area= 300
    print("Based on an effluent area value of", CEFONMA.necessaryEffluentQuality['TSS'])
    print("The Reed Submerged TSS Effluent:", ReedSSF.effluent('TSS'))
    print("The Kadlec Submerged Bed TSS Effluent:", KadlecSSF_kC.safeFunctionCall("effluent", 'TSS'))

    CEFONMA.area = 1000
    print("Based on an effluent area value of", CEFONMA.necessaryEffluentQuality['TSS'])
    print("The Reed Submerged Bed TSS Effluent:", ReedSSF.effluent('TSS'))
    print("The Kadlec Submerged Bed TSS Effluent:", KadlecSSF_kC.safeFunctionCall("effluent", 'TSS'))
    """
    
    output.printAreaGraph(ReedSSF, 'BOD', 10, 800, [155, 286])
    output.printAreaGraph(ReedFWF, 'BOD', 10, 800, [155, 286])


    output.printAreaGraph(KadlecSSF_PkC, 'BOD', 15, 800, [155, 286])
    output.printAreaGraph(KadlecSSF_kC, 'BOD', 15, 800, [155, 286])
    
 
    
    
    output.printMultipleModelsArea(KadlecSSF_kC, 15, 800, [])
    output.printMultipleModelsArea(ReedSSF, 15, 800, [])
    #output.printMultipleModelsArea(KadlecSSF_PkC, 15, 800, [])

    #output.printMediaCharacteristicsTable(ReedSSF)
    output.printTable21_1(KadlecSSF_kC) 
    
    output.printTableOfEffluent(KadlecSSF_kC, [500, 1000, 10000])

    KadlecSSF_kC.effluent('fecalColiform')
    
    output.printTable('annualAndMonthlyTemps', CEFONMA.climateTemps, title='Annual and Monthly Temps')
    output.printTable('mediaCharacteristicsReed', ReedSSF.mediaCharacteristicsTable, title="Typical Media Characteristics for Subsurface Flow Wetlands")
    output.printTable("annualAndMonthlySnowfall", CEFONMA.snowfall, title="Annual and Monthly Snowfall")
    output.printTable("annualAndMonthlyRainfall", CEFONMA.rainfall, title="Annual and Monthly Rainfall")
    output.printTable("annualAndMonthlyEvapo", CEFONMA.evapotranspiration, title="Annual and Monthly Evapotranspiration")
    output.printTable("firstOrderBODRateConstantsKadlec", KadlecSSF_PkC.tableBODRateConstants, "Summary of First-Order Rate Constants for Selected Parameters")
    output.printTable("firstOrderRateConstantsKadlec", KadlecSSF_PkC.tableRateConstants, "Summary of First-Order Rate Constants for Selected Parameters")


    CEFONMA.avgFlowRate = 20
    CEFONMA.numberOfCells = 4
    CEFONMA.area = 500
    CEFONMA.porosity = 0.38
    CEFONMA.depth = 0.30
    CEFONMA.currentSepticTankEffluent['BOD'] = 200
    CEFONMA.tankArea = 125
    CEFONMA.backgroundEffluent['BOD']
    output.printTable20_1('Table20_1', 'BOD', k=45/365)

    CEFONMA.__init__()
    output.printTable20_1('fourCellArea', 'BOD')

        

if __name__ == '__main__': main()
