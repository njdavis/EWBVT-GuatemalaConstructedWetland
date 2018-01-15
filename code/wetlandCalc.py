"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from classDefinitions import Site, WaterQualityData

def main():
    #Pulling data from wikipedia page about Chajul. Should see if we can find information for a town closer.

    avgChajulTempsByMonth = [14.6,15.1,16.6,17.4,17.5,17.5,16.7,16.7,16.8,16.1,15.7,15.2]

    CEFONMA = Site()
    CEFONMA.temp = avgChajulTempsByMonth
    print(CEFONMA.temp[1])
    print(CEFONMA.tempLength)
    print(CEFONMA.tempAVG)

if __name__ == '__main__': main()
