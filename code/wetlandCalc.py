"""Program to calculate constructed wetland design"""
import sys, math, unittest

#importing class definitions
from siteInfo import Site


class ReedModel:

    #Volumetric Design Equations
    #BOD
    def K_T(self, qualityType, T_W):
        if qualityType == 'BOD':
            K_20 = self.BOD_Const['K_20']
            theta = self.BOD_Const['theta']
        elif qualityType == 'ammonia':
            K_20 = self.ammonia_Const['K_20']
            theta = self.ammonia_Const['theta']
        elif qualityType == 'nitrate':
            K_20 = self.nitrate_Const['K_20']
            theta = self.nitrate_Const['theta']

        return (K_20*theta**(T_W-20))

    def treatmentArea(self, avgFlowRate,influentConcentration, effluentConcentration, K_T):
        return avgFlowRate*((math.log(influentConcentration/effluentConcentration))/(K_T*self.avgDepth*self.porosity))

    def effluent(self, influentConcentration, K_T, t):
        return influentConcentration*math.exp(-K_T*t)

    def phosphorusEffluent(self, influentConcentration, K_P, HLR):
        return influentConcentration*math.exp(-K_P/HLR)

    def fecalColiformRemoval(self, influentConcentration, K_P, HRT, numberOfCells):
        return influentConcentration(1/(1+K_P*HRT)**numberOfCells)

    
class ReedSubsurfaceFlow(ReedModel):

    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.BOD_Const = {'K_20':1.1, 'theta':1.06} 
        self.ammonia_Const = {'K_20':0.4107, 'theta':1.048}
        # For Ammonia: The KNH value would be 0.4107 with a fully developed root zone and 0.01854
        self.nitrate_Const = {'K_20':1, 'theta':1.15} #^From Reed
        self.coliform_Const = {'K_20':0.274, 'theta':1.03} #From kadlec

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8
            
    def TSSEffluent(self, influentConcentration, HLR):
        return influentConcentration*(0.1058+(0.0011*HLR))


class ReedFreewaterFlow(ReedModel):

    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.BOD_Const = {'K_20':0.678, 'theta':1.06} 
        self.ammonia_Const = {'K_20':0.2187, 'theta':1.048}
        self.nitrate_Const = {'K_20':1, 'theta':1.15} #^From Reed
        self.coliform_Const = {'K_20':2.6, 'theta':1.19} #From kadlec

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8

    def TSSEffluent(self, influentConcentration, HLR):
        return influentConcentration*(0.11139+(0.00213*HLR))


#Kadlec Models

class Kadlec():

    #Volumetric Design Equations
    #BOD
    def K_T(self, qualityType, T_W):
        if qualityType == 'BOD':
            K_20 = self.BOD_Const['K_20']
            theta = self.BOD_Const['theta']
        elif qualityType == 'ammonia':
            K_20 = self.ammonia_Const['K_20']
            theta = self.ammonia_Const['theta']
        elif qualityType == 'nitrate':
            K_20 = self.nitrate_Const['K_20']
            theta = self.nitrate_Const['theta']
        elif qualityType == 'coliform':
            K_20 = self.coliform_Const['K_20']
            theta = self.coliform_Const['theta']

        return (K_20*theta**(T_W-20))


    def treatmentArea(self, qualityType, avgFlowRate,influentConcentration, effluentConcentration, K_Tinput):
        if qualityType == 'BOD':
            backgroundConcentration = self.BOD_Const['backgroundConcentration']
        elif qualityType == 'ammonia':
            backgroundConcentration = self.ammonia_Const['backgroundConcentration']
        elif qualityType == 'nitrate':
            backgroundConcentration = self.nitrate_Const['backgroundConcentration']
        elif qualityType == 'organicNitrogen':
            backgroundConcentration = self.organicNitrogen_Const['backgroundConcentration']
        elif qualityType == 'totalNitrogen':
            backgroundConcentration = self.totalNitrogen_Const['backgroundConcentration']
        elif qualityType == 'toalPhosphorus':
            backgroundConcentration = self.totalPhosphorus_Const['backgroundConcentration']
        elif qualityType == 'coliform':
            backgroundConcentration = self.coliform_Const['backgroundConcentration']


        return avgFlowRate*(math.log((influentConcentration - backgroundConcentration)/(effluentConcentration - backgroundConcentration))/(self.K_T(qualityType, K_Tinput)))


class KadlecSubsurfaceFlow(Kadlec):
    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.BOD_Const = {'K_20':0.3205, 'theta':1.057, 'backgroundConcentration':3.0}
        self.TSS_Const = {'k_20':0.1186, 'theta':1.00, 'backgroundConcentration':6.0}
        self.organicNitrogen_Const = {'k_20':0.0959, 'theta':1.05, 'backgroundConcentration':1.5}
        self.ammonia_Const = {'K_20':0.0932, 'theta':1.05, 'backgroundConcentration':0}
        # For Ammonia: The KNH value would be 0.4107 with a fully developed root zone and 0.01854
        self.nitrate_Const = {'K_20':0.1370, 'theta':1.05, 'backgroundConcentration':0} #^From Reed
        self.totalNitrogen_Const = {'K_20':0.0274, 'theta':1.05, 'backgroundConcentration':1.5}
        self.totalPhospohorus_Const = {'K_20':0.0249, 'theta':1.097, 'backgroundConcentration':0}
        self.coliform_Const = {'K_20':0.274, 'theta':1.03, 'backgroundConcentration':200} #From kadlec

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8


  
