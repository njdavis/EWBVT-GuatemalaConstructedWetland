import  unittest, math
from siteInfo import Site
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow


#This is an example of how a testing module would be set up. But tests aren't actually useful for anything right now
class VolumetricProcessModelTest(unittest.TestCase):
   
    reedFreewaterFlow = ReedFreewaterFlow()
    CEFONMA = Site()

    #testing that the K_T function is correct
    def testK_T(self):
                
        self.reedFreewaterFlow.KT_Const['BOD'] = 0.678
        self.reedFreewaterFlow.theta_Const['BOD'] = 1.06
        test = self.reedFreewaterFlow.K_T('BOD',20)

        self.assertEqual(test, .678)

    def testTreatmentAreaBOD(self):
       
        self.CEFONMA.avgFlowRate = 18
        self.CEFONMA.currentSepticTankEffluent['BOD'] = 1625
        self.CEFONMA.waterTemp = 20
        self.CEFONMA.necessaryEffluentQuality['BOD'] = 1.84645

        self.reedFreewaterFlow.avgDepth = 0.4
        self.reedFreewaterFlow.porosity = 0.7
        self.reedFreewaterFlow.KT_Const['BOD'] = 0.678
        self.reedFreewaterFlow.theta_Const['BOD'] = 1.06
     
        test = self.reedFreewaterFlow.treatmentArea('BOD', self.CEFONMA)

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 642.857, 3)

    def testTreatmentAreaAmmonia(self):
        
        self.CEFONMA.avgFlowRate = 18
        self.CEFONMA.currentSepticTankEffluent['ammonia'] = 32
        self.CEFONMA.waterTemp = 20
        self.CEFONMA.necessaryEffluentQuality['ammonia'] = 10.7213

        self.reedFreewaterFlow.avgDepth = 0.4
        self.reedFreewaterFlow.porosity = 0.7
        self.reedFreewaterFlow.KT_Const['ammonia'] = 0.2187
        self.reedFreewaterFlow.theta_Const['ammonia'] = 1.048

        test = self.reedFreewaterFlow.treatmentArea('ammonia', self.CEFONMA)

        #checks to 3 decimal places
        self.assertAlmostEqual(test, 321.430, 3)

    def testTreatmentAreaNitrate(self):
        
        self.CEFONMA.avgFlowRate = 18
        self.CEFONMA.currentSepticTankEffluent['nitrate'] = 32
        self.CEFONMA.waterTemp = 20
        self.CEFONMA.necessaryEffluentQuality['nitrate'] = 0.215614

        self.reedFreewaterFlow.avgDepth = 0.4
        self.reedFreewaterFlow.porosity = 0.7
        self.reedFreewaterFlow.KT_Const['nitrate'] = 1
        self.reedFreewaterFlow.theta_Const['nitrate'] = 1.15

        test = self.reedFreewaterFlow.treatmentArea('nitrate', self.CEFONMA)

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

