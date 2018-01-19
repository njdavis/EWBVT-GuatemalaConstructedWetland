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
        test = reedModel.K_T('BOD',t_w)

        self.assertEqual(test, .678)

    def testTreatmentAreaBOD(self):
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

        test = reedModel.treatmentArea(CEFONMA.flowRate, CEFONMA.waterQualityData['BOD'], effluentConcentration, reedModel.K_T('BOD',t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 642.857, 3)

    def testTreatmentAreaAmmonia(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        CEFONMA.flowRate = 18
        CEFONMA.waterQualityData['ammonia'] = 32
        effluentConcentration = 10.7213

        reedModel.avgDepth = 0.4
        reedModel.porosity = 0.7
        reedModel.ammonia_Const['K_20'] = 0.2187
        reedModel.ammonia_Const['theta'] = 1.048
        t_w = 20

        test = reedModel.treatmentArea(CEFONMA.flowRate, CEFONMA.waterQualityData['ammonia'], effluentConcentration, reedModel.K_T('ammonia',t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 321.430, 3)

    def testTreatmentAreaNitrate(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        CEFONMA.flowRate = 18
        CEFONMA.waterQualityData['nitrate'] = 32
        effluentConcentration = 0.215614

        reedModel.avgDepth = 0.4
        reedModel.porosity = 0.7
        reedModel.ammonia_Const['K_20'] = 1
        reedModel.ammonia_Const['theta'] = 1.15
        t_w = 20

        test = reedModel.treatmentArea(CEFONMA.flowRate, CEFONMA.waterQualityData['nitrate'], effluentConcentration, reedModel.K_T('nitrate',t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 321.429, 3)

    def testBODEffluent(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        CEFONMA.waterQualityData['BOD'] = 1625
        t = 8

        reedModel.BOD_Const['K_20'] = 0.678
        reedModel.BOD_Const['theta'] = 1.06
        t_w = 20

        test = reedModel.effluent(CEFONMA.waterQualityData['BOD'], reedModel.K_T('BOD', t_w), t)
        #checks to 3 decimal places
        self.assertAlmostEqual(test, 7.165, 3)

    def testTSSEffluent(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()

        test = reedModel.TSSEffluent(14, 7.4675)

        self.assertAlmostEqual(test, 1.81726, 3)

    def testNitrateEffluent(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        CEFONMA.waterQualityData['nitrate'] = 32
        t = 5
    
        reedModel.nitrate_Const['K_20'] = 1
        reedModel.nitrate_Const['theta'] = 1.15
        t_w = 20

        test = reedModel.effluent(CEFONMA.waterQualityData['nitrate'], reedModel.K_T('nitrate', t_w), t)
        #checks to 3 decimal places
        self.assertAlmostEqual(test, 0.215614, 3)

    def testPhosphorusEffluent(self):
        reedModel = VolumetricProcessDesignModel()
        CEFONMA = Site()
        CEFONMA.flowRate = 18
        CEFONMA.waterQualityData['Phosphorus'] = 7.76
        
        K_P = 2.73
        HLR = 5
        test = reedModel.phosphorusEffluent(CEFONMA.waterQualityData['Phosphorus'], K_P, HLR)

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 4.49507, 3)



if __name__ == '__main__':
    unittest.main()

