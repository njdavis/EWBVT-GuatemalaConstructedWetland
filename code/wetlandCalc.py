"""Program to calculate constructed wetland design"""
import sys, math, unittest

#importing class definitions
from siteInfo import Site


class VolumetricProcessDesignModel:


    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.BOD_Const = {'K_20':0.678, 'theta':1.06}

        #self.effluentConcentration = 10

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8


    #Volumetric Design Equations
    def K_T(self, T_W):
        return (self.BOD_Const['K_20']*self.BOD_Const['theta']**(T_W-20))

    def treatmentArea(self, avgFlowRate,influentConcentration, effluentConcentration, K_T):
        return avgFlowRate*((math.log(influentConcentration/effluentConcentration))/(K_T*self.avgDepth*self.porosity))

"""

#example of how to use class
reedModel = VolumetricProcessDesignModel()
CEFONMA = Site()
print(reedModel.K_T(18))
print(reedModel.treatmentArea(CEFONMA.flowRate, CEFONMA.waterQualityData['BOD'], 10,  reedModel.K_T(18)))
"""

