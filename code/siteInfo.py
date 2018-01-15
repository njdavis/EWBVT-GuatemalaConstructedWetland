#Class created to store information about the site (ie, CEFONMA Water Flow rates)

class Site:

    #initialize values
    def __init__(self):
        #initialized with high end of EPA concentrations in typical residential wastewater
        #can be found at /EWBVT-GuatemalaConstructedWetland/sources/EPA\ Document\ About\ Leach\ Fields.pdf 
        #values in mg/L
        self.BOD = 286
        self.TSS = 880
        self.ammonia = 13
        self.nitrogen = 75
        self.waterQualityList = [0,880,0,0]

        #initialized with average monthly chajul temps (https://en.wikipedia.org/wiki/Chajul). Update if we find a closer town
        self.monthlyTemps = [14.6,15.1,16.6,17.4,17.5,17.5,16.7,16.7,16.8,16.1,15.7,15.2]

        #initialized with CEFONMA's current wastewater flow, according to EPA
        self.flowRate = 5,625

        #initialized with the current location of CEFONMA
        self.coordinates = {'latitude':15.47, 'longitude':-91.09}

        #initialize with elevation of CEFONMA (meters) found using google maps
        self.elevation = 2152.62

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
        self.monthlyTemps = newTemps

    def printMonthlyTemps(self):
        print ("January:%.1f, February:%.1f, March:%.1f, April:%.1f, May:%.1f, June:%.1f, July:%.1f, August:%.1f, September:%.1f, October:%.1f, November:%.1f, December:%.1f" % (self.monthlyTemps[0], self.monthlyTemps[1],self.monthlyTemps[2],self.monthlyTemps[3],self.monthlyTemps[4],self.monthlyTemps[5], self.monthlyTemps[6],self.monthlyTemps[7],self.monthlyTemps[8],self.monthlyTemps[9],self.monthlyTemps[10], self.monthlyTemps[11]))

    def updateFlowRate(self, newFlow):
        self.flowRate = newFlow

    def updateElevation(self, newElev):
        self.elevation = newElev



"""

#Sample of how class is used

CEFONMA = Site()
CEFONMA.updateWaterQualityData(6,4,3,2)
CEFONMA.updateNitrogen(3)
CEFONMA.printWaterQuality()
CEFONMA.updateFlowRate(20250)
CEFONMA.printMonthlyTemps()
print(CEFONMA.waterQualityList)
print(CEFONMA.flowRate)
print(CEFONMA.coordinates)

"""
