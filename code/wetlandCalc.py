"""Program to calculate constructed wetland design"""
import sys, math, unittest

#importing class definitions
from siteInfo import Site
import matplotlib.pyplot as plt

class PresentData():

    def printAreaGraph(self, waterQualityParameter, site, waterQualityLow, waterQualityHigh,  highlightedValuesX):
        '''
        Prints graphs about how changing certain water quality parameters changes the area needed
        waterQualityParameter=string, site = siteInfo(), waterQualityLow = int, waterQualityHigh = int, highlightedValues = [x,..]
        '''
        
        waterQualityList = []
        yAxis = []
        xAxis = []
        areaEPA = []
        
        for value in range(waterQualityLow, waterQualityHigh):
            xAxis.append(value) 
            site.currentSepticTankEffluent[waterQualityParameter] = value
            yAxis.append(self.treatmentArea(waterQualityParameter, site))

        outputPlot = plt.figure()
         
        outputSubPlot = outputPlot.add_subplot(111)
        for parameterValue in highlightedValuesX:
            site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            outputSubPlot.annotate('(%d, %d)' % (parameterValue, self.treatmentArea(waterQualityParameter, site)), xy=(parameterValue+30, self.treatmentArea(waterQualityParameter, site)-20 ))

            plt.plot(xAxis, yAxis, '-', parameterValue, self.treatmentArea('BOD', site), 'h') 

        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        outputSubPlot.set(title=r'%s' % self.nameOfModel,
        xlabel='%s (%s)' % (waterQualityParameter, units), ylabel= 'Area Required for Constructed Wetland $(m^2)$')


        outputPlot.savefig("../Graphs and Charts/%s-%s.pdf" % (self.nameOfModel, waterQualityParameter), bbox_inches='tight')


class ReedModel(PresentData):
    
    def K_T(self, qualityType, T_W):
        return (self.KT_Const[qualityType]*self.theta_Const[qualityType]**(T_W-20))

    def treatmentArea(self, qualityType, site):
        return site.avgFlowRate*((math.log(site.currentSepticTankEffluent[qualityType]/site.necessaryEffluentQuality[qualityType]))/(self.K_T(qualityType, site.waterTemp)*self.avgDepth*self.porosity))

    def effluent(self, K_T, t):
        return site.currentSepticTankEffluent*math.exp(-K_T*t)

    def phosphorusEffluent(self, K_P, HLR):
        return site.currentSepticTankEffluent*math.exp(-K_P/HLR)

        
class ReedSubsurfaceFlow(ReedModel):

    def __init__(self): 
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.KT_Const = {'BOD':1.1, 'ammonia':0.4107, 'nitrate':1 }
        self.theta_Const = {'BOD':1.06, 'ammonia':1.048, 'nitrate':1.15 }

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Reed Subsurface Flow"

            
    def TSSEffluent(self, influentConcentration, HLR):
        return influentConcentration*(0.1058+(0.0011*HLR))


class ReedFreewaterFlow(ReedModel):

    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.KT_Const = {'BOD':0.678, 'ammonia':0.2187, 'nitrate':1 }
        self.theta_Const = {'BOD':1.06, 'ammonia':1.048, 'nitrate':1.15 }

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Reed Freewater Flow"

    def TSSEffluent(self, influentConcentration, HLR):
        return influentConcentration*(0.11139+(0.00213*HLR))


#Kadlec Models

class Kadlec(PresentData):

    #Volumetric Design Equations
    #BOD
    def K_T(self, qualityType, T_W):
        return (self.KT_Const[qualityType]*self.theta_Const[qualityType]**(T_W-20))


    def treatmentArea(self, qualityType, siteInfo):  
        return siteInfo.avgFlowRate*(math.log((siteInfo.currentSepticTankEffluent[qualityType] - self.backgroundConcentration[qualityType])/(siteInfo.necessaryEffluentQuality[qualityType] - self.backgroundConcentration[qualityType]))/(self.K_T(qualityType, siteInfo.waterTemp)))

    

class KadlecSubsurfaceFlow(Kadlec):
    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.KT_Const = {'BOD':0.3205, 'TSS':0.1186, 'organicNitrogen':0.959, 'ammonia':0.0932, 'nitrate':0.1370, 'totalNitrogen':0.0274, 'totalPhosphorus':0.0249, 'fecalColiform':0.274}
        self.theta_Const = {'BOD':1.057, 'TSS':1, 'organicNitrogen':1.05, 'ammonia':1.05, 'nitrate':1.05, 'totalNitrogen':1.05, 'totalPhosphorus':1.097, 'fecalColiform':1.03}
        self.backgroundConcentration = {'BOD':3.0, 'TSS':6.0, 'organicNitrogen':1.5, 'ammonia':0, 'nitrate':0, 'totalNitrogen':1.5, 'totalPhosphorus':0, 'fecalColiform':200}
        # For Ammonia: The KNH value would be 0.4107 with a fully developed root zone and 0.01854
        
        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Kadlec Subsurface Flow"


          
