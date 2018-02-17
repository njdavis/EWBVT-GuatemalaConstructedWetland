"""Program to calculate constructed wetland design"""
import sys, math, unittest, tabulate

#importing class definitions
from siteInfo import Site
from present import PresentData


class Wetland():

    def __init__(self, CEFONMA):
        self.reedSSF = ReedSubsurfaceFlow(CEFONMA)
        self.reedFWS = ReedFreewaterFlow(CEFONMA)
        self.kadlec1996SSF = Kadlec1996SSF(CEFONMA)
        self.kadlec2009SSF = Kadlec2009SSF(CEFONMA)
        self.output = PresentData(CEFONMA)
        

        self.model = self.kadlec2009SSF

        self.wetlandType = 'SSF'

        self.SSFmodelList = {'reed':self.reedSSF, 'kadlec2009':self.kadlec2009SSF, 'kadlecPkC':self.kadlec2009SSF, 'kadlec1996':self.kadlec1996SSF, 'kadleckC':self.kadlec1996SSF}
        self.FWSmodelList = {'reed':self.reedFWS}
        
    def changeWetlandType(self, newType):
        self.wetlandType = newType            

    def changeModel(self, newModel):
        if self.wetlandType == 'SSF':
            self.model = self.SSFmodelList[newModel]
        elif self.wetlandType == 'FWS':
            self.model = self.FWSmodelList[newModel]
        else:
            print("Not a proper model or wetland type")
        return

    #Area Calls
    def area(self, qualityType):
        if self.model.nameOfModel == "Kadlec kC SSF":
            return self.model.safeFunctionCall(area, qualityType)
        else:
            return  self.model.area(qualityType)

    def printArea(self, qualityType):
        if self.model.nameOfModel == "Kadlec kC SSF":
            print("The %s Bed Area (m^2): %f" % (self.model.nameOfModel, self.model.safeFunctionCall(area, qualityType)))
        else:
            print("The %s Bed Area (m^2): %f" % (self.model.nameOfModel, self.model.area(qualityType)))

    
    #Effluent Calls   
    def effluent(self, qualityType):
        if self.model.nameOfModel == "Kadlec kC SSF":
            return self.model.safeFunctionCall(effluent, qualityType)
        else:
            return  self.model.effluent(qualityType)
        
    def printEffluent(self, qualityType):
        if self.model.nameOfModel == "Kadlec kC SSF":
            print("The %s Bed Effluent (m^2): %f" % (self.model.nameOfModel, self.model.safeFunctionCall(effluent, qualityType)))
        else:
            print("The %s Bed Effluent (m^2): %f" % (self.model.nameOfModel, self.model.effluent(qualityType)))

    #Print table of Results
    def printTableOfCalcs(self, qualityType, filename=None):
        if filename is None:
            self.output.printTableOfCalcs('BOD', self.model)
        else:
            self.output.printTableOfCalcs('BOD', self.model, filename=filename)





#Virtual Class of the Reed Model
class ReedModel():
    
    def K_T(self, qualityType):
        return (self.KT_Const[qualityType]*self.theta_Const[qualityType]**(self.site.waterTemp-20))

    def area(self, qualityType):
        return self.site.avgFlowRate*((math.log(self.site.currentSepticTankEffluent[qualityType]/self.site.necessaryEffluentQuality[qualityType]))/(self.K_T(qualityType)*self.avgDepth*self.porosity))

            
            
class ReedSubsurfaceFlow(ReedModel):

    def __init__(self, site): 
        self.site = site
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.worksFor = ['BOD', 'TSS',  'ammonia', 'nitrate', 'fecalColiform']
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

    def hydrolicLoadingRate(self):
        return ((self.site.avgFlowRate)/self.site.area)*100

    def effluent(self, qualityType):
        hydrolicLoadingRate = self.hydrolicLoadingRate()
        hydrolicRetentionTime = (self.site.area*self.site.depth*self.site.porosity)/self.site.avgFlowRate

        #Gotta reread the book to figure out 
        if qualityType == 'TSS':
            if hydrolicLoadingRate < 0.4:
                #print("Hydrolic Loading Rate %d Too Low" % hydrolicLoadingRate)
                hydrolicLoadingRate = 0.4
            elif hydrolicLoadingRate > 75:
                #print("Hydrolic Loading Rate %d Too High" % hydrolicLoadingRate)
                hydrolicLoadingRate = 75
                
            return self.site.currentSepticTankEffluent[qualityType]*(0.1058+(0.0011*hydrolicLoadingRate))
        else:
            return self.site.currentSepticTankEffluent[qualityType]*math.exp(-self.K_T(qualityType)*hydrolicRetentionTime)

class ReedFreewaterFlow(ReedModel):

    def __init__(self, site):
        self.site = site
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.worksFor = {'BOD', 'TSS',  'ammonia', 'nitrate', 'phosphorus'}
        self.KT_Const = {'BOD':0.678, 'ammonia':0.2187, 'nitrate':1 }
        self.theta_Const = {'BOD':1.06, 'ammonia':1.048, 'nitrate':1.15 }

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

        self.nameOfModel = "Reed Freewater Flow"

    def effluent(self, qualityType):
        hydrolicLoadingRate = self.site.avgFlowRate/self.site.area

        if qualityType == 'phosphorus':
            return self.site.currentSepticTankEffluent*math.exp(-self.K_T(qualityType, self.site.waterTemp)/hydrolicLoadingRate)
        elif qualityType == 'TSS':
            return self.site.currentSepticTankEffluent[qualityType]*(0.11139+(0.00213*hydrolicLoadingRate))
        else:
            return self.site.currentSepticTankEffluent[qualityType]*math.exp(-self.K_T(qualityType, site.waterTemp)*self.hydrolicRetentionTime)

#Virtual Class of the Kadlec Models
class Kadlec():

    #Volumetric Design Equations
    def backgroundConcentration(self, qualityType): 
        return (self.background_Const[qualityType]*self.theta_Const[qualityType]**(self.site.waterTemp-20))

    def area(self, qualityType):  
        hectares = ((0.0365*self.site.avgFlowRate)/self.k_Const[qualityType])*math.log((self.site.currentSepticTankEffluent[qualityType] - self.backgroundConcentration(qualityType))/(self.site.necessaryEffluentQuality[qualityType] - self.backgroundConcentration(qualityType)) )
        return hectares*10000
      
    def isEffluentQualityTooLow(self, qualityType):
        if self.backgroundConcentration(qualityType) > self.site.necessaryEffluentQuality[qualityType]:
            isEffluentTooLow = True
        else: 
            isEffluentTooLow = False   
        return isEffluentTooLow

    def safeFunctionCall(self, function, qualityType):
        if self.isEffluentQualityTooLow(qualityType):
            print("Your effluent %s requirements are too low for this %s influent value (%.2f vs %.2f). Change area or C_in" % (qualityType, qualityType, self.site.necessaryEffluentQuality[qualityType], self.backgroundConcentration(qualityType)))
            return 0
        else:
            if function == 'area':
                return self.area(qualityType)
            else:
                return self.effluent(qualityType)

    def minNecessaryEffluentQuality(self):
        listOfMinValues = []
        for qualityType in self.background_Const:
            listOfMinValues.append(self.background_Const[qualityType])  
        return listOfMinValues

    def effluent(self, qualityType):
        a = self.backgroundConcentration(qualityType)
        b = (self.site.currentSepticTankEffluent[qualityType] - self.backgroundConcentration(qualityType))
        c = -(self.k_Const[qualityType]*(self.site.area/10000))/(0.0365*self.site.avgFlowRate)
        return a + b*math.exp(c)
        

class Kadlec1996SSF(Kadlec):
    def __init__(self, site): 
        self.site = site

        self.worksFor = ['BOD', 'TSS', 'organicNitrogen', 'ammonia', 'nitrate', 'totalNitrogen', 'totalPhosphorus', 'fecalColiform']
        
        
        self.regression_Const = {'BOD':[0.33,1.4], 
                                 'TSS':[7.8, 0.063], 
                                 'organicNitrogen':[0.6], 
                                 'ammonia':[3.3, 0.46], 
                                 'totalNitrogen':[2.6, 0.46, 0.124], 
                                 'totalPhosphorus':[0.51, 1.1]}

        self.background_Const = {'BOD':(3.5+0.053*self.site.currentSepticTankEffluent['BOD']),
                                 'TSS':(7.8+0.063*self.site.currentSepticTankEffluent['TSS']), 
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

        self.nameOfModel = "Kadlec kC SSF"

        #for tss 1000 is a rough estimate, should figure out settling rate instead
        self.worksForAbb = ('BOD', 'TSS', 'Organic N', 'NH~4~-N', 'NO~x~N', 'TN', 'TP', 'FC')


class Kadlec2009SSF(Kadlec):

    def __init__(self, site):

        self.site = site

        self.tableBODRateConstants = {"**C~i~ (mg/L)**":["**FWS**", "P", "C^\*^, (mg/L)", "30th %ile  (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)", "  ", "**HSSF**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)", " ",  "**VFSF**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)"], 
                "**BOD Tertiary 0-30 (mg/L)**":[" ",1, 2, 16, 33, 79, " ", " ",3, 1, 36, 86, 224, " ", " ",6,0,22,63,105], 
                "**BOD Tertiary 30-100 (mg/L)**":[" ",1,5,16,'**41**',67," "," ",3,5,24,'**37**',44, " ", " ",6,0,40,"**56**",79], 
                "**BOD Tertiary 100-200 (mg/L)**":[" ",1,10,23,'**36**',112," "," ",3,10,15,'**25**',44, " ", " ",6,0,53,"**76**",122], 
                "**BOD Tertiary >200 (mg/L)**":[" ",1,20,54,189,439," "," ",3,15,21,66,114, " ", " ",6,0,48,71,93]}
        
        self.tableRateConstants = {"**C~i~ (mg/L)**":["**FWS**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)", "  ", "**HSSF**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)"], 
        "**ORG-N**":[" ",3,1.5,10.7,'**17.3**',27.4," "," ",6,1,8.8,'**19.6**',38.0], 
        "**NH~4~-N**":[" ",3,0,8.7,'**14.7**',45.1," "," ",6,0,5.2,'**11.4**',18.8], 
        "**NO~x~-N**":[" ",3,0,18.5,'**26.5**',33.6," "," ",8,0,32,'**42**',73], 
        "**TKN**":[" ",3,1.5,6.1,'**9.8**',13.6," "," ",6,1,4.8,'**9.1**',14.6], 
        "**TN**":[" ",3,1.5,6.6,'**12.6**',24.2," "," ",6,1,4.7,'**8.4**',14.2], 
        "**TP**":[" ",3.4,0.002,4.5,'**10.0**',16.7," "," ","*","*","*","*","*"], 
        "**FC**":[" ",3,40,49,'**83**',177," "," ",6,0,56,'**103**',181]}

        self.k_Const = {'BOD':76/365, 'organicNitrogen':19.6/365, 'ammonia':11.4/365, 'nitrate':42/365, 'totalNitrogen':9.1/365, 'fecalColiform':103/365} 

        self.theta_Const =      {'BOD':1.0, 
                                 'TSS':1.0, 
                                 'organicNitrogen':1.05, 
                                 'ammonia':1.04, 
                                 'nitrate':1.09, 
                                 'totalNitrogen':1.05, 
                                 'totalPhosphorus':1, 
                                 'fecalColiform':1}

        self.background_Const = {'BOD':8}
        

        self.worksFor = ['BOD']

        self.nameOfModel = "Kadlec PkC SSF"


    #Volumetric Design Equations
    def area(self, qualityType, cells=None, k=None, c_i=None):   
        if cells is None:
            cells = self.site.numberOfCells
        if k is None:
            k = self.k_Const[qualityType]
        if c_i is None:
            c_i=self.site.currentSepticTankEffluent[qualityType]

        x = (c_i-self.site.backgroundEffluent[qualityType])/(self.site.necessaryEffluentQuality[qualityType]-self.site.backgroundEffluent[qualityType])  
        metersCubed = ((cells*self.site.avgFlowRate)*((x)**(1/cells) - 1))/k
        return metersCubed
      
    def effluent(self, qualityType, cells=None, area=None, k=None):
        if cells is None:
            cells = self.site.numberOfCells
        if area is None:
            area = self.site.area
        if k is None:
            k = self.k_Const[qualityType]

        a = (self.site.currentSepticTankEffluent[qualityType] - self.site.backgroundEffluent[qualityType])
        b = (1+(k/(cells*(self.site.avgFlowRate/area))))**cells
        return a/b + self.site.backgroundEffluent[qualityType]
        



