"""Program to calculate constructed wetland design"""
import sys

#importing class definitions
from siteInfo import Site
import wetlandCalc

def main():

    CEFONMA = Site()
    CEFONMA.printMonthlyTemps()


if __name__ == '__main__': main()
