import  unittest, math
from siteInfo import SiteData
from wetlandCalc import KadlecSSF, KadlecSSF_BOD, KadlecSSF_TSS, KadlecSSF_OrganicNitrogen, KadlecSSF_Ammonia, KadlecSSF_TotalNitrogen, KadlecSSF_Nitrate, KadlecSSF_FecalColiform, Wetland

class KadlecEquationTest(unittest.TestCase):
    
    def setUp(self):
        #setDefault Values before every test
        self.data = SiteData() 

        self.data.avgFlowRate = 20
        self.data.numberOfCells = 4
        self.data.area = 500
        self.data.porosity = 0.38
        self.data.depth = 0.3 

        self.data.influentQuality['BOD'] = 200
        self.data.backgroundEffluentQuality['BOD'] = 8
        self.data.necessaryEffluentQuality['BOD'] = 30

        self.data.influentQuality  = {   
            'BOD':200, 
            'TSS':200, 
            'organicNitrogen':200, 
            'ammonia':200, 
            'nitrate':200, 
            'totalNitrogen':200, 
            'totalPhosphorus':200, 
            'fecalColiform':200
        }

        self.data.backgroundEffluentQuality = {  
            'BOD':8,
            'TSS':8, 
            'organicNitrogen':8, 
            'ammonia':8, 
            'nitrate':8, 
            'totalNitrogen':8, 
            'totalPhosphorus':8, 
            'fecalColiform':8
        }

        self.data.necessaryEffluentQuality = {   
            'BOD':30, 
            'TSS':30,                
            'organicNitrogen':30, 
            'ammonia':30, 
            'nitrate':30, 
            'totalNitrogen':30, 
            'totalPhosphorus':30, 
            'fecalColiform':30
        }

        self.k_Const = 45/365

    #WETLAND ######################################
    def testSetCriteria(self):
        wetland = Wetland(self.data)
        wetland.setCriteriaType('TSS')
        tempKadlecSSF = KadlecSSF_TSS(self.data)

        self.assertEqual(wetland.wetlandType, 'SSF')
        self.assertEqual(wetland.getArea(), tempKadlecSSF.getArea())
    
    #BOD ##########################################
    def testEffluentBOD(self):
        BOD = KadlecSSF_BOD(self.data)
        BOD.setK_Const(self.k_Const)
        result = BOD.getEffluent()

        self.assertAlmostEqual(result, 27.5, 1)

    def testAreaBOD(self):
        BOD = KadlecSSF_BOD(self.data)
        BOD.setK_Const(self.k_Const)
        result = BOD.getArea()

        self.assertAlmostEqual(result, 466.4, 1) #Need to check this is the right answer

    #TSS ###########################################
    def testAreaTSS(self):
        TSS = KadlecSSF_TSS(self.data)
        TSS.setK_Const(self.k_Const)
        result = TSS.getArea()

        self.assertEqual(result, "Area cannot be calculated based on TSS")

    def testEffluentTSS(self):
        TSS = KadlecSSF_TSS(self.data)
        TSS.setK_Const(self.k_Const)
        result = TSS.getEffluent()

        self.assertEqual(result, 45.5)

    #ORGANIC NITROGEN ##############################
    def testAreaOrganicNitrogen(self):
        organicNitrogen = KadlecSSF_OrganicNitrogen(self.data)
        organicNitrogen.setK_Const(self.k_Const)
        result = organicNitrogen.getArea()

        self.assertAlmostEqual(result, 466.4, 1) #Need to check this is the right answer

    def testEffluentOrganicNitrogen(self):
        organicNitrogen = KadlecSSF_OrganicNitrogen(self.data)
        organicNitrogen.setK_Const(self.k_Const)
        result = organicNitrogen.getEffluent()

        self.assertAlmostEqual(result, 27.5, 1)

    #AMMONIA #######################################
    def testAreaAmmonia(self):
        ammonia = KadlecSSF_Ammonia(self.data)
        ammonia.setK_Const(self.k_Const)
        result = ammonia.getArea()

        self.assertAlmostEqual(result, 466.4, 1) #Need to check this is the right answer

    def testEffluentAmmonia(self):
        ammonia = KadlecSSF_Ammonia(self.data)
        ammonia.setK_Const(self.k_Const)
        result = ammonia.getEffluent()

        self.assertAlmostEqual(result, 27.5, 1)

    #TOTAL NITROGEN  #######################################
    def testAreaAmmonia(self):
        totalNitrogen = KadlecSSF_TotalNitrogen(self.data)
        totalNitrogen.setK_Const(self.k_Const)
        result = totalNitrogen.getArea()

        self.assertAlmostEqual(result, 466.4, 1) #Need to check this is the right answer

    def testEffluentAmmonia(self):
        totalNitrogen = KadlecSSF_TotalNitrogen(self.data)
        totalNitrogen.setK_Const(self.k_Const)
        result = totalNitrogen.getEffluent()

        self.assertAlmostEqual(result, 27.5, 1)

    #AMMONIA #######################################
    def testAreaNitrate(self):
        nitrate = KadlecSSF_Nitrate(self.data)
        nitrate.setK_Const(self.k_Const)
        result = nitrate.getArea()

        self.assertAlmostEqual(result, 466.4, 1) #Need to check this is the right answer

    def testEffluentAmmonia(self):
        nitrate = KadlecSSF_Nitrate(self.data)
        nitrate.setK_Const(self.k_Const)
        result = nitrate.getEffluent()

        self.assertAlmostEqual(result, 27.5, 1)

    #FECAL COLIFORM #######################################
    def testAreaAmmonia(self):
        fecalColiform = KadlecSSF_FecalColiform(self.data)
        fecalColiform.setK_Const(self.k_Const)
        result = fecalColiform.getArea()

        self.assertAlmostEqual(result, 466.4, 1) #Need to check this is the right answer

    def testEffluentAmmonia(self):
       	fecalColiform = KadlecSSF_FecalColiform(self.data)
        fecalColiform.setK_Const(self.k_Const)

        result = fecalColiform.getEffluent()

        self.assertAlmostEqual(result, 27.5, 1)



if __name__ == '__main__':
    unittest.main()

