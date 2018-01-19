"""Program to calculate constructed wetland design"""
import sys, math, unittest

#importing class definitions
from siteInfo import Site


class VolumetricProcessDesignModel:


    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.BOD_Const = {'K_20':0.678, 'theta':1.06}
        self.ammonia_Const = {'K_20':0.2187, 'theta':1.048}
        self.nitrate_Const = {'K_20':1, 'theta':1.15}

        #self.effluentConcentration = 10

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8


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

"""

#example of how to use class
reedModel = VolumetricProcessDesignModel()
CEFONMA = Site()
print(reedModel.K_T(18))
print(reedModel.treatmentArea(CEFONMA.flowRate, CEFONMA.waterQualityData['BOD'], 10,  reedModel.K_T(18)))
"""

