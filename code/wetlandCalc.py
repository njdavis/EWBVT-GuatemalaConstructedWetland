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
    def backgroundConcentration(self, qualityType, site):
        return (self.background_Const[qualityType]*self.theta_Const[qualityType]**(site.waterTemp-20))

    def area(self, qualityType, site):  
        hectares = ((0.0365*site.avgFlowRate)/self.k_Const[qualityType])*math.log((site.currentSepticTankEffluent[qualityType] - self.backgroundConcentration(qualityType, site))/(site.necessaryEffluentQuality[qualityType] - self.backgroundConcentration(qualityType, site)) )
        return hectares*10000
      
    def isEffluentQualityTooLow(self, qualityType, site):
        if self.backgroundConcentration(qualityType, site) > site.necessaryEffluentQuality[qualityType]:
            isEffluentTooLow = True
        else: 
            isEffluentTooLow = False   
        return isEffluentTooLow

    def safeFunctionCall(self, function, qualityType, site):
        if self.isEffluentQualityTooLow(qualityType, site):
            print("Your effluent %s requirements are too low for this %s influent value (%.2f vs %.2f). Change area or C_in" % (qualityType, qualityType, site.necessaryEffluentQuality[qualityType], self.backgroundConcentration(qualityType, site)))
            return 0
        else:
            if function == 'area':
                return self.area(qualityType, site)
            else:
                return self.effluent(qualityType, site)

    def minNecessaryEffluentQuality(self, site):
        listOfMinValues = []
        for qualityType in self.background_Const:
            listOfMinValues.append(self.background_Const[qualityType])  
        return listOfMinValues

    def effluent(self, qualityType, site):
        a = self.backgroundConcentration(qualityType, site)
        b = (site.currentSepticTankEffluent[qualityType] - self.backgroundConcentration(qualityType, site))
        c = -(self.k_Const[qualityType]*(site.area/10000))/(0.0365*site.avgFlowRate)
        return a + b*math.exp(c)
        

class KadlecSubsurfaceFlow(Kadlec):
    def __init__(self, site): 

        self.worksFor = ('BOD', 'TSS', 'organicNitrogen', 'ammonia', 'nitrate', 'totalNitrogen', 'totalPhosphorus', 'fecalColiform')
        
        
        self.regression_Const = {'BOD':[0.33,1.4], 
                                 'TSS':[7.8, 0.063], 
                                 'organicNitrogen':[0.6], 
                                 'ammonia':[3.3, 0.46], 
                                 'totalNitrogen':[2.6, 0.46, 0.124], 
                                 'totalPhosphorus':[0.51, 1.1]}

        self.background_Const = {'BOD':(3.5+0.053*site.currentSepticTankEffluent['BOD']),
                                 'TSS':(7.8+0.063*site.currentSepticTankEffluent['TSS']), 
                                 'organicNitrogen':1.5, 
                                 'ammonia':0, 
                                 'nitrate':0, 
                                 'totalNitrogen':1.5, 
                                 'totalPhosphorus':0.02, 
                                 'fecalColiform':10} 
                                 #fecal coliform: 10^b of central tendency of widely variable value

        self.theta_Const =      {'BOD':1.0, 
                                 'TSS':1.0, 
                                 'organicNitrogen':1.05, 
                                 'ammonia':1.04, 
                                 'nitrate':1.09, 
                                 'totalNitrogen':1.05, 
                                 'totalPhosphorus':1, 
                                 'fecalColiform':1} 

        self.k_Const =          {'BOD':180, 
                                 'TSS':1000, 
                                 'organicNitrogen':35, 
                                 'ammonia':34, 
                                 'nitrate':50, 
                                 'totalNitrogen':27, 
                                 'totalPhosphorus':12, 
                                 'fecalColiform':95}

        
        
        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Kadlec Subsurface Flow"

        #for tss 1000 is a rough estimate, should figure out settling rate instead
        self.worksForAbb = ('BOD', 'TSS', 'Organic N', 'NH~4~-N', 'NO~x~N', 'TN', 'TP', 'FC')

    def convertBackground_Const(self):
        out = self.regression_Const
        for value in self.worksFor:
            if value == 'BOD':
                out[value] = "3.5+0.053 C~i~"
            elif value == 'TSS':
                out[value] = "7.8+0.063 C~i~"
            else:
                out[value] = str(self.background_Const[value])
        return out

    def table21_1(self):
        convBackground_Const = self.convertBackground_Const()
        out = []
        for x, qualityType in enumerate(self.worksFor):
            out.append([])
            out[x].append(str(self.k_Const[qualityType]))
            out[x].append(str(self.theta_Const[qualityType]))
            out[x].append(convBackground_Const[qualityType])

        return out
    
    def printTable21_1(self):
        values = self.table21_1()
        #from table 21-1: SSF Model Parameter Values -- Preliminary
        self.SSFModelParmaters = {"": ["k20, m/yr", "$\Theta$", "C*, mg/L"], "BOD":values[0], "TSS":values[1], "Organic N":values[2], 'NH~4~-N':values[3] , 'NO~x~N':values[4], 'TN':values[5], 'TP':values[6], 'FC':values[7]}

        text_file = open("../Graphs and Charts/charts/Kadlec 21-1 Table.txt", "w")
        text_file.write(tabulate.tabulate(self.SSFModelParmaters, headers="keys", tablefmt="simple"))
        text_file.write("\n \nTable: Typical Media Characteristics for Subsurface Flow Wetlands {#tbl:MediaCharacteristicsReed}")
        text_file.close()



            


