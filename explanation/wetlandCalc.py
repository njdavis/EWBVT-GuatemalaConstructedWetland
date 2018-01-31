"""Program to calculate constructed wetland design"""
import sys, math, unittest, tabulate

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

        #from table 7.1: Media Characteristics
        self.hCLow = [328*0.305, 1640*0.305, 3280*0.305, 32800*0.305, 164000*0.305]
        self.hCHigh = [3280*0.305, 16400*0.305, 32800*0.305, 164000*0.305, 820000*0.305]
        self.hydraulicConductivity = []
        for low, high in zip(self.hCLow, self.hCHigh):
            self.hydraulicConductivity.append("%s - %s" % (round(low, 2), round(high, 2)))

        self.mediaCharacteristicsTable = {"Media Type": ["Coarse Sand", "Gravelly Sand", "Fine Gravel", "Medium Gravel", "Coarse Rock"], "Effective Size (D~10~)(mm)": [2, 8, 16, 32, 128], "Porosity (n)(%)":["28-32","30-35","35-38","36-40","38-45"], "Hydraulic Conductivity (K~s~)(m/d)":self.hydraulicConductivity}

    def printMediaCharacteristicsTable(self):
        text_file = open("../Graphs and Charts/charts/Media Characteristics Table.txt", "w")
        text_file.write(tabulate.tabulate(self.mediaCharacteristicsTable, headers="keys", tablefmt="simple"))
        text_file.write("\n \nTable: Typical Media Characteristics for Subsurface Flow Wetlands {#tbl:MediaCharacteristicsReed}")
        text_file.close()



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
        self.C*_Const = {'BOD':0.678, 'ammonia':0.2187, 'nitrate':1 }
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
    def backgroundConentration(self, qualityType, T_W):
        return (self.background_Const[qualityType]*self.theta_Const[qualityType]**(T_W-20))

    def treatmentArea(self, qualityType, siteInfo):  
        return siteInfo.avgFlowRate*(math.log((siteInfo.currentSepticTankEffluent[qualityType] - self.backgroundConcentration[qualityType])/(siteInfo.necessaryEffluentQuality[qualityType] - self.backgroundConcentration[qualityType]))/(self.K_T(qualityType, siteInfo.waterTemp)))

    def effluent(self, qualityType, siteInfo):
        return (self.backgroundConentration(qualityType) + (siteInfo.currentSepticTankEffluent[qualityType] - self.backgroundConentration(qualityType))*math.log(-(self.k_Const[qualityType]*siteInfo.area)/(0.0365*self.siteInfo.avgFlowRate)))        
    

class KadlecSubsurfaceFlow(Kadlec):
    def __init__(self, siteInfo):

        self.worksFor = ('BOD', 'TSS', 'organicNitrogen', 'ammonia', 'nitrate', 'totalNitrogen', 'totalPhosphorus')
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.backgroundConcentration_Const = {'BOD':(3.5+0.053*siteInfo.currentSepticTankEffluent['BOD']), 'TSS':(7.8+0.063*siteInfo.currentSepticTankEffluent['TSS'], 'organicNitrogen':1.5, 'ammonia':0, 'nitrate':0, 'totalNitrogen':1.5, 'totalPhosphorus':0.02, 'fecalColiform':0} #fecal coliform: 10^b of central tendency of widely variable value
        self.theta_Const = {'BOD':1.0, 'TSS':1.065, 'organicNitrogen':1, 'ammonia':1, 'nitrate':1, 'totalNitrogen':1, 'totalPhosphorus':1, 'fecalColiform':1}
       
        # For Ammonia: The KNH value would be 0.4107 with a fully developed root zone and 0.01854
        
        self.regression_Const = {'BOD':[0.33,1.4], 'TSS':[7.8, 0.063], 'organicNitrogen':[0.6], 'ammonia':[3.3, 0.46], 'totalNitrogen':[2.6, 0.46, 0.124], 'totalPhosphorus':[0.51, 1.1]}
        
        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Kadlec Subsurface Flow"

        self.k_Const = {'BOD':180, 'TSS':1000, 'organicNitrogen':35, 'ammonia':34, 'nitrate':50, 'totalNitrogen':27, 'totalPhosphorus':12, 'fecalColiform':95}
        #for tss 1000 is a rough estimate, should figure out settling rate instead

          

#Virtual Class of the Kadlec Models
class Tanzania():

    #Volumetric Design Equations
    #BOD
    def K_T(self, qualityType, T_W):
        return (self.backgroundConcentration_Const[qualityType]*self.theta_Const[qualityType]**(T_W-20))

    def treatmentArea(self, qualityType, siteInfo):  
        return ((0.0365*siteInfo.avgFlowRate)/self.k[qualityType])*math.log((siteInfo.currentSepticTankEffluent[qualityType] - backgroundConcentration(qualityType))/(siteInfo.necessaryEffluentQuality[qualityType] - backgroundConcentration(qualityType)))
        
    def effluent(self, qualityType, siteInfo):
        hydrolicLoadingRate = siteInfo.avgFlowRate/siteInfo.area
        return (math.exp((-self.K_T(qualityType, siteInfo.waterTemp)/hydrolicLoadingRate)))*(siteInfo.currentSepticTankEffluent[qualityType] + (math.exp(self.K_T(qualityType, siteInfo.waterTemp)/hydrolicLoadingRate)*self.backgroundConcentration[qualityType]) - self.backgroundConcentration[qualityType])
        
    

class TanzaniaSubsurfaceFlow(Tanzania):
    def __init__(self):

        self.worksFor = ('BOD', 'TSS', 'organicNitrogen', 'ammonia', 'nitrate', 'totalNitrogen', 'totalPhosphorus')
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.KT_Const = {'BOD':3.5, 'TSS':0.1186, 'organicNitrogen':0.959, 'ammonia':0.0932, 'nitrate':0.1370, 'totalNitrogen':0.0274, 'totalPhosphorus':0.0249, 'fecalColiform':0.274}
        self.theta_Const = {'BOD':1.057, 'TSS':1, 'organicNitrogen':1.05, 'ammonia':1.05, 'nitrate':1.05, 'totalNitrogen':1.05, 'totalPhosphorus':1.097, 'fecalColiform':1.03}
        self.backgroundConcentration = {'BOD':3.0, 'TSS':6.0, 'organicNitrogen':1.5, 'ammonia':0, 'nitrate':0, 'totalNitrogen':1.5, 'totalPhosphorus':0, 'fecalColiform':200}
        # For Ammonia: The KNH value would be 0.4107 with a fully developed root zone and 0.01854
        
        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Kadlec Subsurface Flow"


          
