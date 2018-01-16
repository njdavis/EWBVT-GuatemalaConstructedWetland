import unittest
from siteInfo import Site
from wetlandCalc import VolumetricProcessDesignModel


#This is an example of how a testing module would be set up. But tests aren't actually useful for anything right now
class VolumetricProcessModelTest(unittest.TestCase):

    def testCalculation(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()

        test1 = reedModel.treatmentArea(CEFONMA.flowRateM3PD(), CEFONMA.waterQualityData['BOD'], reedModel.K_T(18))

        self.assertEqual(test1, 1)

class VolumetricProcessModelTest1(unittest.TestCase):

    def testCalculation1(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()

        test1 = reedModel.treatmentArea(CEFONMA.flowRateM3PD(), CEFONMA.waterQualityData['BOD'], reedModel.K_T(18))

        self.assertEqual(test1, 295.7989894526602)



if __name__ == "__main__": 
    unittest.main()
