#Class created to store information about the site (ie, CEFONMA Water Flow rates)
import math

class Site:

    #initialize values
    def __init__(self):
        #initialized with high end of EPA concentrations in typical residential wastewater
        #can be found at /EWBVT-GuatemalaConstructedWetland/sources/EPA\ Document\ About\ Leach\ Fields.pdf 
        #values in mg/L
        self.currentSepticTankEffluent = {'BOD':168, 'TSS':85, 'organicNitrogen':0.1, 'ammonia':40, 'nitrate':0.1, 'totalNitrogen':63.4, 'totalPhosphorus':8.1, 'fecalColiform':10**6}
        self.necessaryEffluentQuality = {'BOD':10, 'TSS':10, 'organicNitrogen':10, 'ammonia':10, 'nitrate':10, 'totalNitrogen':10, 'totalPhosphorus':10, 'fecalColiform':200}


        #initialized with average monthly chajul temps (https://en.wikipedia.org/wiki/Chajul). Update if we find a closer town
        self.monthlyTemps = [14.6,15.1,16.6,17.4,17.5,17.5,16.7,16.7,16.8,16.1,15.7,15.2]

        #initialized with CEFONMA's current wastewater flow, according to EPA (m^3/day)
        self.avgFlowRate = 76.65

        #20250 = 76.65 possible future flowrate
        #5625 = 17.74 - 21.29 current flowrate

        self.waterTemp = 18

        #initialized with the current location of CEFONMA
        self.coordinates = {'latitude':15.47, 'longitude':-91.09}

        #initialize with elevation of CEFONMA (meters) found using google maps
        self.elevation = 2152.62

        self.area = 822
        

    def flowRateM3PD(self):
        return self.flowRate*0.003785

    #Use water quality data as a list
    def outputWaterQuality(self):
        return [self.currentSepticTankEffluentQuality['BOD'], self.currentSepticTankEffluentQuality['TSS'],self.currentSepticTankEffluentQuality['ammonia'], self.currentSepticTankEffluentQuality['nitrogen'], self.currentSepticTankEffluentQuality['phosphorus']]

    def updateWaterQuality(self, data):
        self.currentSepticTankEffluentQuality['BOD'] = data[0]
        self.currentSepticTankEffluentQuality['TSS'] = data[1]
        self.currentSepticTankEffluentQuality['ammonia'] = data[2]
        self.currentSepticTankEffluentQuality['nitrogen'] = data[3]
        self.currentSepticTankEffluentQuality['phosphorus'] = data[4]

    #Print functions
    def printMonthlyTemps(self):
        print ("January:%.1f, February:%.1f, March:%.1f, April:%.1f, May:%.1f, June:%.1f, July:%.1f, August:%.1f, September:%.1f, October:%.1f, November:%.1f, December:%.1f" % (self.monthlyTemps[0], self.monthlyTemps[1],self.monthlyTemps[2],self.monthlyTemps[3],self.monthlyTemps[4],self.monthlyTemps[5], self.monthlyTemps[6],self.monthlyTemps[7],self.monthlyTemps[8],self.monthlyTemps[9],self.monthlyTemps[10], self.monthlyTemps[11]))


    def printWaterQuality(self):
        print ("BOD:%d TSSS:%d Ammonia:%d Nitrogen:%d Phosphorus:%d" % (self.currentSepticTankEffluentQuality['BOD'], self.currentSepticTankEffluentQuality['TSS'],self.currentSepticTankEffluentQuality['ammonia'], self.currentSepticTankEffluentQuality['nitrogen'], self.currentSepticTankEffluentQuality['phosphorus']))

