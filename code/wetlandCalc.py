"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from siteInfo import Site

def main():

    CEFONMA = Site()
    print(CEFONMA.temp[1])
    print(CEFONMA.tempLength)
    print(CEFONMA.tempAVG)

if __name__ == '__main__': main()
