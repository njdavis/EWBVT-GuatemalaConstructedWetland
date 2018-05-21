"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import Wetland
from present import PresentData

def main():
    
    #Example of how to initialize values
    CEFONMA = Site() #This stores all values related to wetland design
    wetland = Wetland(CEFONMA) #This calculates values, using CEFONMA as input

    #Examples of changing all CEFONMA Values
    CEFONMA.avgFlowRate = 20
    CEFONMA.numberOfCells = 4
    CEFONMA.area = 500
    CEFONMA.porosity = 0.38
    CEFONMA.depth = 0.30
    CEFONMA.currentSepticTankEffluent['BOD'] = 200
    CEFONMA.tankArea = 125
    CEFONMA.backgroundEffluent['BOD']
    

    
    wetland.printTableOfAreaCalcs('BOD')

    CEFONMA.__init__() 

    wetland.printCurrentInputs()
    wetland.printTableOfEffluents()
    
    

if __name__ == '__main__': main()
