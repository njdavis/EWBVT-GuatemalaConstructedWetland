"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import Wetland
from present import PresentData

def main():
    
<<<<<<< HEAD
    #Example of how to initialize values
    CEFONMA = Site() #This stores all values related to wetland design
    wetland = Wetland(CEFONMA) #This calculates values, using CEFONMA as input
     
    #Examples of how to printing out calculated values
=======
    CEFONMA = Site()    
    wetland = Wetland(CEFONMA) # site info only

    
    #Examples of graphs being printed
    CEFONMA.area = 300
    CEFONMA.currentSepticTankEffluent['BOD'] = 200
>>>>>>> 9c23b33c7cf231963db5d0f9d4c1c497bf24dd5f
    wetland.printArea('BOD')
    wetland.printEffluent('BOD')

    #Examples of how to changing input values 
    CEFONMA.currentSepticTankEffluent['BOD'] = 150
    CEFONMA.necessaryEffluentQuality['BOD'] = 30
    wetland.printArea('BOD')
    CEFONMA.area = 300
    wetland.printEffluent('ammonia') 

    #Example of how to print table of calculations
    wetland.printTableOfCalcs('BOD')

    #Examples of how to print 
    wetland.printChangingWaterQualityGraph('BOD')
    wetland.printChangingAreaGraph()

    #Examples of changing all CEFONMA Values
    CEFONMA.avgFlowRate = 20
    CEFONMA.numberOfCells = 4
    CEFONMA.area = 500
    CEFONMA.porosity = 0.38
    CEFONMA.depth = 0.30
    CEFONMA.currentSepticTankEffluent['BOD'] = 200
    CEFONMA.tankArea = 125
    CEFONMA.backgroundEffluent['BOD']
    wetland.printPDFTableOfCalcs('BOD',filename='Table20_1', k=45/365)

    #Example of how to reset CEFONMA to default values
    CEFONMA.__init__()
    wetland.printPDFTableOfCalcs('BOD', filename='fourCellArea')

    #Example of how to print all current inputs stored in CEFONMA
    wetland.printCurrentInputs()
    
    

if __name__ == '__main__': main()
