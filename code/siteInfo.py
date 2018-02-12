#Class created to store information about the site (ie, CEFONMA Water Flow rates)
import math

class Site:

    #initialize values
    def __init__(self):
        #initialized with high end of EPA concentrations in typical residential wastewater
        #can be found at /EWBVT-GuatemalaConstructedWetland/sources/EPA\ Document\ About\ Leach\ Fields.pdf 
        #values in mg/L
        self.currentSepticTankEffluent = {'BOD':168, 'TSS':85, 'organicNitrogen':10, 'ammonia':40, 'nitrate':30, 'totalNitrogen':30, 'totalPhosphorus':8.1, 'fecalColiform':10**6}
        self.necessaryEffluentQuality = {'BOD':30, 'TSS':30, 'organicNitrogen':2, 'ammonia':0.1, 'nitrate':2, 'totalNitrogen':2, 'totalPhosphorus':0.05, 'fecalColiform':200}
        self.backgroundEffluent = {'BOD':8}


        #initialized with average monthly chajul data (https://en.wikipedia.org/wiki/Chajul). Update if we find a closer town
        self.climateTemps = {'Jan':14.6,'Feb':15.1,'Mar':16.6,'Apr':17.4,'May':17.5,'Jun':17.5,'Jul':16.7,'Aug':16.7,'Sep':16.8,'Oct':16.1,'Nov':15.7,'Dec':15.2, 'Annual':16.33}

        self.snowfall = {'Jan':"__",'Feb':"__",'Mar':"__",'Apr':"__",'May':"__",'Jun':"__",'Jul':"__",'Aug':"__",'Sep':"__",'Oct':"__",'Nov':"__",'Dec':"__", 'Annual':"__"}
        self.rainfall = {'Jan':65,'Feb':42,'Mar':50,'Apr':66,'May':128,'Jun':306,'Jul':264,'Aug':230,'Sep':251,'Oct':224,'Nov':127,'Dec':64, 'Annual':1818}
        self.evapotranspiration = {'Jan':"__",'Feb':"__",'Mar':"__",'Apr':"__",'May':"__",'Jun':"__",'Jul':"__",'Aug':"__",'Sep':"__",'Oct':"__",'Nov':"__",'Dec':"__", 'Annual':"__"}

        self.waterTemp = 18

        #initialized with the current location of CEFONMA
        self.coordinates = {'latitude':15.47, 'longitude':-91.09}

        #initialize with elevation of CEFONMA (meters) found using google maps
        self.elevation = 2152.62

        #initialized with CEFONMA's current wastewater flow, according to EPA (m^3/day)
        self.avgFlowRate = 76.65

        #20250 = 76.65 possible future flowrate
        #5625 = 17.74 - 21.29 current flowrate

        #Design Numbers
        self.numberOfCells = 6
        self.porosity = 0.8
        self.depth = 0.5

        self.area = 1000
        self.tankArea = self.area/self.numberOfCells
         

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

