"""Program to calculate constructed wetland design"""
import sys, math

class Wetland():
    def __init__(self, data):
        self.data = data
        self.wetlandType = 'SSF'
        self.model = KadlecSSF_BOD(self.data)

    def setCriteriaType(self, criteriaType):
        if criteriaType is 'BOD':
            self.model = KadlecSSF_BOD(self.data)
        elif criteriaType is 'TSS':
            self.model = KadlecSSF_TSS(self.data)
        elif criteriaType is 'organicNitrogen':
            self.model = KadlecSSF_OrganicNitrogen(self.data)
        elif criteriaType is 'ammonia':
            self.model = KadlecSSF_Ammonia(self.data)
        elif criteriaType is 'totalNitrogen':
            self.model = KadlecSSF_TotalNitrogen(self.data)
        elif criteriaType is 'nitrate':
            self.model = KadlecSSF_Nitrate(self.data)
        elif criteriaType is 'fecalColiform':
            self.model = KadlecSSF_FecalColiform(self.data)
 
    def getArea(self):
        return self.model.getArea()

    def getEffluent(self):
        return self.model.getEffluent()


class KadlecSSF():
    def __init__(self, data):
        self.data = data
        self.nameOfModel = "Kadlec PkC SSF"
        self.k_Const = -1
        self.background_Const = -1

    def initializeData(self, criteriaType):
        self.cells = self.data.numberOfCells
        self.area = self.data.area
        self.flowRate = self.data.avgFlowRate
        self.influentQuality = self.data.influentQuality[criteriaType]
        self.backgroundEffluentQuality = self.data.backgroundEffluentQuality[criteriaType]
        self.necessaryEffluentQuality = self.data.necessaryEffluentQuality[criteriaType]


    def getArea(self):
        x = (self.influentQuality-self.backgroundEffluentQuality)/(self.necessaryEffluentQuality-self.backgroundEffluentQuality)  
        metersCubed = ((self.cells*self.flowRate)*((x)**(1/self.cells) - 1))/self.k_Const
        return metersCubed


    def getEffluent(self):        
        numerator = self.influentQuality - self.backgroundEffluentQuality
        denominator = (1+(self.k_Const/(self.cells*(self.flowRate/self.area))))**self.cells
        return numerator/denominator + self.backgroundEffluentQuality

    def setK_Const(self, newK_Const):
        self.k_Const = newK_Const

class KadlecSSF_BOD(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.k_Const = 76/365
        self.initializeData('BOD')

        
class KadlecSSF_TSS(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.initializeData('TSS')
        
    #Need to add error try catch
    def getArea(self):
        return "Area cannot be calculated based on TSS"
        

    def getEffluent(self):
        TSSEffluent = 1.5+0.22*self.influentQuality
        if TSSEffluent < self.backgroundEffluentQuality:
            return self.backgroundEffluentQuality
        else: 
            return TSSEffluent

class KadlecSSF_OrganicNitrogen(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.k_Const = 19.6/365
        self.initializeData('organicNitrogen')

        
class KadlecSSF_Ammonia(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.k_Const = 11.4/365
        self.initializeData('ammonia')

        
class KadlecSSF_TotalNitrogen(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.k_Const = 9.1/365
        self.initializeData('totalNitrogen')

class KadlecSSF_Nitrate(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.k_Const = 42/365
        self.initializeData('nitrate')

class KadlecSSF_FecalColiform(KadlecSSF):
    def __init__(self, data):
        self.data = data
        self.k_Const = 103/365
        self.initializeData('fecalColiform')

"""
class KadlecSSF_TotalPhosphorus(KadlecSSF):
    def __init__(self, data, k=None):
        default_k_Const =
        self.optionalKInput(default_k_Const, k)
        self.initializeData('totalPhosphorus')
"""

