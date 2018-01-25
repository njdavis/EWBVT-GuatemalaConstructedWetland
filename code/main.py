"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
import matplotlib.pyplot as plt
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow

def main():

    CEFONMA = Site()    
    #Reed = ReedSubsurfaceFlow()
    Kadlec = KadlecSubsurfaceFlow()
    
    print("Kadlec Area needed (with BOD = 155): %d m^2" % Kadlec.treatmentArea('BOD', CEFONMA))

"""
    kadlecBODX = []
    kadlecBODY = []
    BODEPA = [155,286]
    areaEPA = [Kadlec.treatmentArea('BOD', CEFONMA.flowRate, lowEPABOD, 10, 18), Kadlec.treatmentArea('BOD', CEFONMA.flowRate, highEPABOD, 10, 18)]

    for BOD in range(10, 500):
        xAxis.append(BOD) 
        yAxis.append(Kadlec.treatmentArea('BOD', CEFONMA.flowRate, BOD, 10, 18))

    changingBOD = plt.figure()
    

        
    changingBODSub = changingBOD.add_subplot(111)
    for x, BOD in enumerate(BODEPA):
        changingBODSub.annotate('(%d, %d)' % (BOD+20, areaEPA[x]-60), xy=(BOD+20, areaEPA[x]-60))

    plt.plot(xAxis, yAxis, '-', [155, 286], [Kadlec.treatmentArea('BOD', CEFONMA.flowRate, 155, 10, 18), Kadlec.treatmentArea('BOD', CEFONMA.flowRate, 286, 10, 18)], 'h') 

    changingBODSub.set(title=r'How Changing BOD5 Effects Necessary Area of Wetland',
       xlabel='Biological Oxygen Demand (mg/L)', ylabel= 'Area Required for Constructed Wetland $(m^2)$')




    changingBOD.savefig("Graph of BOD Values.pdf", bbox_inches='tight')
       

def printAreaGraph(waterQualityList, waterQualityParameter, temperatureOfWater, flowRate,  xlabel, ylabel, title, highlightedValues):
    '''
    Prints graphs about how changing certain water quality parameters changes the area needed
    waterQualityList=list, waterQualityParameter=string, temperatureOfWater=int (C), flowRate = int (m^2), xlabel=string, ylabel=string, title=string, highlightedValues = [[x,..],[y,..]]
    '''
    
    yAxis = []
    areaEPA = [Kadlec.treatmentArea(waterQualityParameter, flowRate, lowEPABOD, 10, temperatureOfWater), Kadlec.treatmentArea('BOD', flowRate, highEPABOD, 10, temperatureOfWater)]

    for parameter in waterQualityList:
        xAxis.append(BOD) 
        yAxis.append(Kadlec.treatmentArea('BOD', CEFONMA.flowRate, BOD, 10, 18))

    changingBOD = plt.figure()
    

        
    changingBODSub = changingBOD.add_subplot(111)
    for x, BOD in enumerate(BODEPA):
        changingBODSub.annotate('(%d, %d)' % (BOD+20, areaEPA[x]-60), xy=(BOD+20, areaEPA[x]-60))

    plt.plot(xAxis, yAxis, '-', [155, 286], [Kadlec.treatmentArea('BOD', CEFONMA.flowRate, 155, 10, 18), Kadlec.treatmentArea('BOD', CEFONMA.flowRate, 286, 10, 18)], 'h') 

    changingBODSub.set(title=r'How Changing BOD5 Effects Necessary Area of Wetland',
       xlabel='Biological Oxygen Demand (mg/L)', ylabel= 'Area Required for Constructed Wetland $(m^2)$')




    changingBOD.savefig("Graph of BOD Values.pdf", bbox_inches='tight')
"""



if __name__ == '__main__': main()
