"""Program to calculate constructed wetland design"""
import sys, math, unittest

#importing class definitions
from siteInfo import Site

#Virtual Class of the Reed Model
class ReedModel():
    
    def K_T(self, qualityType, T_W):
        return (self.KT_Const[qualityType]*self.theta_Const[qualityType]**(T_W-20))

    def treatmentArea(self, qualityType, site):
        return site.avgFlowRate*((math.log(site.currentSepticTankEffluent[qualityType]/site.necessaryEffluentQuality[qualityType]))/(self.K_T(qualityType, site.waterTemp)*self.avgDepth*self.porosity))

            
class ReedSubsurfaceFlow(ReedModel):

    def __init__(self): 
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.worksFor = {'BOD', 'TSS',  'ammonia', 'nitrate'}
        self.KT_Const = {'BOD':1.104, 'ammonia':0.4107, 'nitrate':1 }
        self.theta_Const = {'BOD':1.06, 'ammonia':1.048, 'nitrate':1.15 }

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Reed Subsurface Flow"

    def hydrolicLoadingRate(self, site):
        return ((site.area*self.avgDepth*self.porosity)/site.avgFlowRate)/100

    def effluent(self, qualityType, site):
        hydrolicLoadingRate = self.hydrolicLoadingRate(site)
        hydrolicRetentionTime = (site.area*self.avgDepth*self.porosity)/site.avgFlowRate

        if qualityType == 'TSS':
            if hydrolicLoadingRate < 0.4:
                hydrolicLoadingRate = 0.4
            return site.currentSepticTankEffluent[qualityType]*(0.1058+(0.0011*hydrolicLoadingRate))
        else:
            return site.currentSepticTankEffluent[qualityType]*math.exp(-self.K_T(qualityType, site.waterTemp)*hydrolicRetentionTime)

class ReedFreewaterFlow(ReedModel):

    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.worksFor = {'BOD', 'TSS',  'ammonia', 'nitrate', 'phosphorus'}
        self.KT_Const = {'BOD':0.678, 'ammonia':0.2187, 'nitrate':1 }
        self.theta_Const = {'BOD':1.06, 'ammonia':1.048, 'nitrate':1.15 }

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Reed Freewater Flow"

    def effluent(self, qualityType, site):
        hydrolicLoadingRate = site.avgFlowRate/site.area

        if qualityType == 'phosphorus':
            return site.currentSepticTankEffluent*math.exp(-self.K_T(qualityType, site.waterTemp)/hydrolicLoadingRate)
        elif qualityType == 'TSS':
            return site.currentSepticTankEffluent[qualityType]*(0.11139+(0.00213*hydrolicLoadingRate))
        else:
            return site.currentSepticTankEffluent[qualityType]*math.exp(-self.K_T(qualityType, site.waterTemp)*self.hydrolicRetentionTime)

#Virtual Class of the Kadlec Models
class Kadlec():

    #Volumetric Design Equations
    #BOD
    def K_T(self, qualityType, T_W):
        return (self.KT_Const[qualityType]*self.theta_Const[qualityType]**(T_W-20))

    def treatmentArea(self, qualityType, siteInfo):  
        return siteInfo.avgFlowRate*(math.log((siteInfo.currentSepticTankEffluent[qualityType] - self.backgroundConcentration[qualityType])/(siteInfo.necessaryEffluentQuality[qualityType] - self.backgroundConcentration[qualityType]))/(self.K_T(qualityType, siteInfo.waterTemp)))

    def effluent(self, qualityType, siteInfo):
        hydrolicLoadingRate = siteInfo.avgFlowRate/siteInfo.area
        return (math.exp((-self.K_T(qualityType, siteInfo.waterTemp)/hydrolicLoadingRate)))*(siteInfo.currentSepticTankEffluent[qualityType] + (math.exp(self.K_T(qualityType, siteInfo.waterTemp)/hydrolicLoadingRate)*self.backgroundConcentration[qualityType]) - self.backgroundConcentration[qualityType])
        
    

class KadlecSubsurfaceFlow(Kadlec):
    def __init__(self):

        self.worksFor = ('BOD', 'TSS', 'organicNitrogen', 'ammonia', 'nitrate', 'totalNitrogen', 'totalPhosphorus')
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


          
