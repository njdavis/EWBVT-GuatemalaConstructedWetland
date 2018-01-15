#Basic class definitions for Water Quality data. 
#To use this file include "import classDefinitions.py"


#BOD, TSS, Ammonia, and Nitrogen levels.

class WaterQualityData:
    def __init__(self,BOD,TSS,Ammonia,Nitrogen):
        self.BOD = BOD
        self.TSS = TSS
        self.Ammonia = Ammonia
        self.Nitrogen = Nitrogen

    #updates all water quality data
    def updateBOD(self, newBOD):
        self.BOD = newBOD

    def updateTSS(self, newTSS):
        self.TSS = newTSS

    def updateAmmonia(self, newAmmonia):
        self.Ammonia = newAmmonia

    def updateNitrogen(self, newNitrogen):
        self.Nitrogen = newNitrogen

    #overrides print function
    def __repr__(self):
        return "BOD:%d TSSS:%d Ammonia:%d Nitrogen:%d" % (self.BOD, self.TSS,self.Ammonia, self.Nitrogen)


""" Sample to show how class is used


test = WaterQualityData(5,4,3,2)
test.updateNitrogen(3)
print(test)

listTest = []
for x in range(0,3):
    listTest.append(WaterQualityData(x+1,x+2,x+3,x+4))
for row in listTest:
    print(row)

"""


#Basic class used to define basic CEFONMA information (Temp, etc.)

class Site:
    def __init__(self):
        self

    #Used to save a list of the temperatures at the school
    def temp(self, a_list):
        for item in a_list:
            print(item)

""" Sample to show how class is used

avgChajulTempsByMonth = [14.6,15.1,6.6,17.4,17.5,17.5,16.7,16.7,16.8,16.1,15.7,15.2]

CEFONMA = Site()
Site.temp = avgChajulTempsByMonth
print(CEFONMA.temp[0])
"""
