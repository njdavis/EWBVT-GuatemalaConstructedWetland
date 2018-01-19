import  unittest, math
from siteInfo import Site
from wetlandCalc import VolumetricProcessDesignModel


#This is an example of how a testing module would be set up. But tests aren't actually useful for anything right now
class VolumetricProcessModelTest(unittest.TestCase):

    #testing that the K_T function is correct
    def testK_T(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        
        reedModel.BOD_Const['K_20'] = 0.678
        reedModel.BOD_Const['theta'] = 1.06
        t_w = 20  
        test1 = reedModel.K_T(t_w)

        self.assertEqual(test1, .678)

    def testTreatmentArea(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        CEFONMA.flowRate = 18
        CEFONMA.waterQualityData['BOD'] = 1625
        effluentConcentration = 1.84645

        reedModel.avgDepth = 0.4
        reedModel.porosity = 0.7
        reedModel.BOD_Const['K_20'] = 0.678
        reedModel.BOD_Const['theta'] = 1.06
        t_w = 20

        test2 = reedModel.treatmentArea(CEFONMA.flowRate, CEFONMA.waterQualityData['BOD'], effluentConcentration, reedModel.K_T(t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test2, 642.857, 3)


if __name__ == '__main__':
    unittest.main()

