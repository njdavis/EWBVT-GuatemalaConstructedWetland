import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import Wetland
from present import PresentData

def main():

    CEFONMA = Site() 
    wetland = Wetland(CEFONMA) 


    functions = ['changeWetlandType(newType)','changeModel(newModel)','area(qualityType)', 'printArea(qualityType)', 'effluent(qualityType)', 'printFffluent(qualityType)']
            
    purposeList = ["Changes between Free Water Surface or Subsurface Wetland","Controls which model is used for calculations", "Calculates necessary area", "Prints area to console", 'Calculates an effluent value for a certain area', 'Prints effluent value to console']
    
    changeWetlandType = [['newType', '"FWS"'],
                         [' ', '"SSF"']]

    changeModel = [['newType', '"reed"'],
                   [' ', '"kadlec2009"'],
                   [' ', '"kadlecPkC"'],
                   [' ', '"kadlec1996"'],
                   [' ', '"KadleckC"']]

    area = [['qualityType', '"BOD"'],
              [' ', '"TSS"'],
              [' ', '"organicNitrogen"'],
              [' ', '"ammonia"'],
              [' ', '"nitrate"'],
              [' ', '"totalNitrogen"'],
              [' ', '"totalPhosphorus"'],
              [' ', '"fecalColiform"'],
              ['cells=', 'integer value'],
              ['k=', 'integer value'],
              ['c_i=', 'integer value']]

    effluent = [['qualityType', '"BOD"'],
                [' ', '"TSS"'],
                [' ', '"organicNitrogen"'],
                [' ', '"ammonia"'],
                [' ', '"nitrate"'],
                [' ', '"totalNitrogen"'],
                [' ', '"totalPhosphorus"'],
                [' ', '"fecalColiform"'],
                ['cells=', 'integer value'],
                ['k=', 'integer value'],
                ['area=', 'integer value']]



    inputList = [changeWetlandType, changeModel, area, area, effluent, effluent]
    wetland.output.printInfoAboutFunctions(functions, purposeList, inputList)
    

if __name__ == '__main__': main()
