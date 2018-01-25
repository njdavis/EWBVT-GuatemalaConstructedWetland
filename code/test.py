import  unittest, math
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow


#This is an example of how a testing module would be set up. But tests aren't actually useful for anything right now
class VolumetricProcessModelTest(unittest.TestCase):
   
    reedModelSubSurface = ReedSubsurfaceFlow()
    CEFONMA = Site()

    #testing that the K_T function is correct
    def testK_T(self):
                
        self.reedModelSubSurface.BOD_Const['K_20'] = 0.678
        self.reedModelSubSurface.BOD_Const['theta'] = 1.06
        t_w = 20  
        test = self.reedModelSubSurface.K_T('BOD',t_w)

        self.assertEqual(test, .678)

    def testTreatmentAreaBOD(self):
       
        self.CEFONMA.flowRate = 18
        self.CEFONMA.waterQualityData['BOD'] = 1625
        effluentConcentration = 1.84645

        self.reedModelSubSurface.avgDepth = 0.4
        self.reedModelSubSurface.porosity = 0.7
        self.reedModelSubSurface.BOD_Const['K_20'] = 0.678
        self.reedModelSubSurface.BOD_Const['theta'] = 1.06
        t_w = 20

        test = self.reedModelSubSurface.treatmentArea(self.CEFONMA.flowRate, self.CEFONMA.waterQualityData['BOD'], effluentConcentration, self.reedModelSubSurface.K_T('BOD',t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 642.857, 3)

    def testTreatmentAreaAmmonia(self):
        
        self.CEFONMA.flowRate = 18
        self.CEFONMA.waterQualityData['ammonia'] = 32
        effluentConcentration = 10.7213

        self.reedModelSubSurface.avgDepth = 0.4
        self.reedModelSubSurface.porosity = 0.7
        self.reedModelSubSurface.ammonia_Const['K_20'] = 0.2187
        self.reedModelSubSurface.ammonia_Const['theta'] = 1.048
        t_w = 20

        test = self.reedModelSubSurface.treatmentArea(self.CEFONMA.flowRate, self.CEFONMA.waterQualityData['ammonia'], effluentConcentration, self.reedModelSubSurface.K_T('ammonia',t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 321.430, 3)

    def testTreatmentAreaNitrate(self):
        
        self.CEFONMA.flowRate = 18
        self.CEFONMA.waterQualityData['nitrate'] = 32
        effluentConcentration = 0.215614

        self.reedModelSubSurface.avgDepth = 0.4
        self.reedModelSubSurface.porosity = 0.7
        self.reedModelSubSurface.ammonia_Const['K_20'] = 1
        self.reedModelSubSurface.ammonia_Const['theta'] = 1.15
        t_w = 20

        test = self.reedModelSubSurface.treatmentArea(self.CEFONMA.flowRate, self.CEFONMA.waterQualityData['nitrate'], effluentConcentration, self.reedModelSubSurface.K_T('nitrate',t_w))

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 321.429, 3)

    def testBODEffluent(self):
        
        self.CEFONMA.waterQualityData['BOD'] = 1625
        t = 8

        self.reedModelSubSurface.BOD_Const['K_20'] = 0.678
        self.reedModelSubSurface.BOD_Const['theta'] = 1.06
        t_w = 20

        test = self.reedModelSubSurface.effluent(self.CEFONMA.waterQualityData['BOD'], self.reedModelSubSurface.K_T('BOD', t_w), t)
        #checks to 3 decimal places
        self.assertAlmostEqual(test, 7.165, 3)

    def testTSSEffluent(self):
        
        test = self.reedModelSubSurface.TSSEffluent(14, 7.4675)

        self.assertAlmostEqual(test, 1.596, 3)

    def testNitrateEffluent(self):
        
        self.CEFONMA.waterQualityData['nitrate'] = 32
        t = 5
    
        self.reedModelSubSurface.nitrate_Const['K_20'] = 1
        self.reedModelSubSurface.nitrate_Const['theta'] = 1.15
        t_w = 20

        test = self.reedModelSubSurface.effluent(self.CEFONMA.waterQualityData['nitrate'], self.reedModelSubSurface.K_T('nitrate', t_w), t)
        #checks to 3 decimal places
        self.assertAlmostEqual(test, 0.215614, 3)

    def testPhosphorusEffluent(self):
        
        self.CEFONMA.flowRate = 18
        self.CEFONMA.waterQualityData['Phosphorus'] = 7.76
        
        K_P = 2.73
        HLR = 5
        test = self.reedModelSubSurface.phosphorusEffluent(self.CEFONMA.waterQualityData['Phosphorus'], K_P, HLR)

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 4.49507, 3)



if __name__ == '__main__':
    unittest.main()

