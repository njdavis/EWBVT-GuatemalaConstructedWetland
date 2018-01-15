"""Program to calculate constructed wetland design"""
import sys
import math

#importing class definitions
from siteInfo import Site


class VolumetricProcessDesignModel:


    def __init__(self):
        #From "Natural Wastewater Treatment Systems". First order removal model
        self.BOD_Const = {'K_20':0.678, 'theta':1.06}

        self.effluentConcentration = 10

        #initialize with reasonable value used in example, but should change this
        self.avgDepth = 0.5

        #initialize to an average value from Reed book
        self.porosity = 0.8


    #Volumetric Design Equations
    def K_T(self, T_W):
        return (self.BOD_Const['K_20']*self.BOD_Const['theta']**(T_W-20))

    def treatmentArea(self, Q_A,influentConcentration, K_T):
        return Q_A(math.log(influentConcentration/self.effluentConcentration)/(K_T*self.avgDepth*self.porosity))



#example of how to use class
reedModel = VolumetricProcessDesignModel()
CEFONMA = Site()
#reedModel.BOD_Const['K_20'] = 20
print(reedModel.treatmentArea(CEFONMA.flowRate,CEFONMA.waterQualityData['BOD'], reedModel.K_T(18)))


