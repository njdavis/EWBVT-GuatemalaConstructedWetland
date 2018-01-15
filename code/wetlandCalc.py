"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from siteInfo import Site


#Volumetric Design Equations
def K_T(K_20,theta, T_W):
    return (K_20*theta**(T_W-20))

test = K_T(0.678,1.06,18)
print(test)

