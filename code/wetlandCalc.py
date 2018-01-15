"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from siteInfo import Site


class VolumetricProcessDesignModel:


    #Volumetric Design Equations
    def K_T(self, K_20,theta, T_W):
        return (K_20*theta**(T_W-20))


test = VolumetricProcessDesignModel()
print(test.K_T(0.678,1.06,18))


