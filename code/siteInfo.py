#Class created to store information about the site (ie, CEFONMA Water Flow rates)

class Site:

    #initialize values
    def __init__(self):
        #initialized with high end of EPA concentrations in typical residential wastewater
        #can be found at /EWBVT-GuatemalaConstructedWetland/sources/EPA\ Document\ About\ Leach\ Fields.pdf 
        #values in mg/L
        self.waterQualityData = {'BOD':286, 'TSS':880, 'ammonia':13, 'nitrogen':75, 'phosphorus':8}

        #initialized with average monthly chajul temps (https://en.wikipedia.org/wiki/Chajul). Update if we find a closer town
        self.monthlyTemps = [14.6,15.1,16.6,17.4,17.5,17.5,16.7,16.7,16.8,16.1,15.7,15.2]

        #initialized with CEFONMA's current wastewater flow, according to EPA (m^3/day)
        self.flowRate = 21.29

        #20250 = 76.65 possible future flowrate
        #5625 = 21.29 current flowrate

        #initialized with the current location of CEFONMA
        self.coordinates = {'latitude':15.47, 'longitude':-91.09}

        #initialize with elevation of CEFONMA (meters) found using google maps
        self.elevation = 2152.62

    def flowRateM3PD(self):
        return self.flowRate*0.003785

    #Use water quality data as a list
    def outputWaterQuality(self):
        return [self.waterQualityData['BOD'], self.waterQualityData['TSS'],self.waterQualityData['ammonia'], self.waterQualityData['nitrogen'], self.waterQualityData['phosphorus']]

    def updateWaterQuality(self, data):
        self.waterQualityData['BOD'] = data[0]
        self.waterQualityData['TSS'] = data[1]
        self.waterQualityData['ammonia'] = data[2]
        self.waterQualityData['nitrogen'] = data[3]
        self.waterQualityData['phosphorus'] = data[4]

    #Print functions
    def printMonthlyTemps(self):
        print ("January:%.1f, February:%.1f, March:%.1f, April:%.1f, May:%.1f, June:%.1f, July:%.1f, August:%.1f, September:%.1f, October:%.1f, November:%.1f, December:%.1f" % (self.monthlyTemps[0], self.monthlyTemps[1],self.monthlyTemps[2],self.monthlyTemps[3],self.monthlyTemps[4],self.monthlyTemps[5], self.monthlyTemps[6],self.monthlyTemps[7],self.monthlyTemps[8],self.monthlyTemps[9],self.monthlyTemps[10], self.monthlyTemps[11]))


    def printWaterQuality(self):
        print ("BOD:%d TSSS:%d Ammonia:%d Nitrogen:%d Phosphorus:%d" % (self.waterQualityData['BOD'], self.waterQualityData['TSS'],self.waterQualityData['ammonia'], self.waterQualityData['nitrogen'], self.waterQualityData['phosphorus']))



"""
#Sample of how class is used

CEFONMA = Site()
print(CEFONMA.waterQualityData)
CEFONMA.updateWaterQuality([4,3,2,1,3])
CEFONMA.printWaterQuality()
CEFONMA.printMonthlyTemps()
print(CEFONMA.waterQualityData)
print(CEFONMA.flowRate)
print(CEFONMA.coordinates)
CEFONMA.printWaterQuality()
"""
