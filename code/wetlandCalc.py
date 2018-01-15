"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from siteInfo import Site


class VolumetricProcessDesignModel:


    def __init__(self):
        #From "Natural Wastewater Treatment Systems"
        self.BOD_Const = {'K_20':0.678, 'theta':1.06}
        #initialize to an average value from Reed book
        self.porosity = 0.8


    #Volumetric Design Equations
    def K_T(self, T_W):
        return (self.BOD_Const['K_20']*self.BOD_Const['theta']**(T_W-20))


test = VolumetricProcessDesignModel()
test.BOD_Const['K_20'] = 20
print(test.K_T(18))


