#Class created to store information about the site (ie, CEFONMA Water Flow rates)
import math

class Site:

    #initialize values
    def __init__(self):
        self.name = 'CEFONMA'
        #initialized with high end of EPA concentrations in typical residential wastewater
        #can be found at /EWBVT-GuatemalaConstructedWetland/sources/EPA\ Document\ About\ Leach\ Fields.pdf 
        #values in mg/L
        self.currentSepticTankEffluent = {'BOD':(168*.6), 'TSS':85, 'organicNitrogen':10, 'ammonia':40, 'nitrate':30, 'totalNitrogen':30, 'totalPhosphorus':8.1, 'fecalColiform':10**6}
        self.necessaryEffluentQuality = {'BOD':30, 'TSS':30, 'organicNitrogen':2, 'ammonia':0.1, 'nitrate':2, 'totalNitrogen':2, 'totalPhosphorus':0.05, 'fecalColiform':200}
        self.backgroundEffluent = {'BOD':(3.5+0.053*self.currentSepticTankEffluent['BOD']),
                                 'TSS':(7.8+0.063*self.currentSepticTankEffluent['TSS']), 
                                 'organicNitrogen':1.5, 
                                 'ammonia':0, 
                                 'nitrate':0, 
                                 'totalNitrogen':1.5, 
                                 'totalPhosphorus':0.02, 
                                 'fecalColiform':10}


        #initialized with average monthly chajul data (https://en.wikipedia.org/wiki/Chajul). Update if we find a closer town
        self.climateTemps = {'Jan':11.6,'Feb':12.1,'Mar':13.6,'Apr':15.6,'May':16.1,'Jun':16.6,'Jul':15.6,'Aug':15.1,'Sep':14.6,'Oct':14.1,'Nov':13.1,'Dec':12.1, 'Annual':16.33}

        self.snowfall = {'Jan':"__",'Feb':"__",'Mar':"__",'Apr':"__",'May':"__",'Jun':"__",'Jul':"__",'Aug':"__",'Sep':"__",'Oct':"__",'Nov':"__",'Dec':"__", 'Annual':"__"}
        self.rainfall = {'Jan':40,'Feb':27,'Mar':37,'Apr':65,'May':116,'Jun':266,'Jul':196,'Aug':183,'Sep':214,'Oct':185,'Nov':86,'Dec':36, 'Annual':1451}
        self.evapotranspiration = {'Jan':40.7,'Feb':40.1,'Mar':54.2,'Apr':65.9,'May':73.3,'Jun':68.8,'Jul':70.7,'Aug':66,'Sep':58.9,'Oct':55.8,'Nov':47.2,'Dec':42.8, 'Annual':684.4}

        self.waterTemp = 18

        #initialized with the current location of CEFONMA
        self.coordinates = {'latitude':15.47, 'longitude':-91.09}

        #initialize with elevation of CEFONMA (meters) found using google maps
        self.elevation = 2120.8

        #initialized with CEFONMA's current wastewater flow, according to EPA (m^3/day)
        self.avgFlowRate = 42.59

        #20,250 = 76.65 possible future flowrate
        #5,625 = 17.74 - 21.29 current flowrate
        #11,250 = 42.59 Double the school's current population

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

