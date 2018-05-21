import  unittest, math
from siteInfo import SiteData
from wetlandCalc import KadlecSSF, KadlecSSF_BOD

class KadlecEquationTest(unittest.TestCase):
    
    def setUp(self):
        #setDefault Values before every test
        self.data = SiteData()
        self.equation = KadlecSSF(SiteData)

        self.data.avgFlowRate = 20
        self.data.numberOfCells = 4
        self.data.area = 500
        self.data.porosity = 0.38
        self.data.depth = 0.3
        self.data.influentQuality['BOD'] = 200
        self.data.backgroundEffluentQuality['BOD'] = 8
        self.data.necessaryEffluentQuality['BOD'] = 30

        self.k = 45/365


    def testEffluentBOD(self):
        self.BOD = KadlecSSF_BOD(self.data, k=self.k)
        result = self.BOD.effluent()

        self.assertAlmostEqual(result, 27.5, 1)
    
    '''
                            'BOD',
                            'TSS',
    'organicNitrogen', 
    'ammonia', 
    'nitrate', 
    'totalNitrogen', 
    'fecalColiform'
    '''


if __name__ == '__main__':
    unittest.main()

