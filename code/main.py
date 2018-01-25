"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow

def main():

    CEFONMA = Site()    
    Reed = ReedSubsurfaceFlow()
    Kadlec = KadlecSubsurfaceFlow()
   
    print(CEFONMA.flowRate)
    print("Area needed (with BOD = 155): %d m^2" % Reed.treatmentArea(CEFONMA.flowRate, 155, 10, Reed.K_T('BOD', 18)))

    print("Area needed (with BOD = 155): %d m^2" % Kadlec.treatmentArea('BOD', CEFONMA.flowRate, 286, 10, 18))

    print("Area needed (with BOD = 286): %d m^2" %Reed.treatmentArea(CEFONMA.flowRate, 286, 10, Reed.K_T('BOD', 18)))

    print("Area needed (for coliform): %d m^2" %Reed.kadlecModel(CEFONMA.flowRate, 37153, 201, 200, Reed.K_T('coliform', 18)))



if __name__ == '__main__': main()
