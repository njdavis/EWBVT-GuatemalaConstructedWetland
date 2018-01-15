#Class created to store information about the site (ie, CEFONMA Water Flow rates)

class SiteInfo:

    #initialize values
    def __init__(self):
        self.BOD = 0
        self.TSS = 0
        self.ammonia = 0
        self.nitrogen = 0
        self.waterQualityList = [0,0,0,0]
        #initialized with average monthly chajul temps. Update if we find a closer town
        self.monthlyTemps = [14.6,15.1,16.6,17.4,17.5,17.5,16.7,16.7,16.8,16.1,15.7,15.2]
        self.flowRate = 5,625 #initialized with CEFONMA's current wastewater flow, according to EPA
        self.coordinates = {'latitude':15.47, 'longitude':-91.09} #initialized with the current location of CEFONMA


    #updates Water Quality Data
    def updateWaterQualityData(self,BOD,TSS,Ammonia,Nitrogen):
        self.waterQualityList = [BOD, TSS, Ammonia, Nitrogen]
        self.BOD = BOD
        self.TSS = TSS
        self.ammonia = Ammonia
        self.nitrogen = Nitrogen

    def updateBOD(self, newBOD):
        self.BOD = newBOD
        self.waterQualityList[0] = newBOD

    def updateTSS(self, newTSS):
        self.TSS = newTSS
        self.waterQualityList[1] = newTSS

    def updateAmmonia(self, newAmmonia):
        self.ammonia = newAmmonia
        self.waterQualityList[2] = newAmmonia

    def updateNitrogen(self, newNitrogen):
        self.nitrogen = newNitrogen
        self.waterQualityList[3] = newNitrogen

    def printWaterQuality(self):
        print ("BOD:%d TSSS:%d Ammonia:%d Nitrogen:%d" % (self.BOD, self.TSS,self.ammonia, self.nitrogen))

    def updateMonthlyTemperatures(self, newTemps):
        self.monthlyTemperatures = newTemps

    def updateFlowRate(self, newFlow):
        self.flowRate = newFlow





"""

#Sample of how class is used

CEFONMA = SiteInfo()
CEFONMA.updateWaterQualityData(6,4,3,2)
CEFONMA.updateNitrogen(3)
CEFONMA.printWaterQuality()
CEFONMA.updateFlowRate(20250)
print(CEFONMA.waterQualityList)
print(CEFONMA.flowRate)
print(CEFONMA.coordinates)

"""
