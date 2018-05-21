"""Program to calculate constructed wetland design"""
import sys, math, unittest, tabulate



class KadlecSSF():
    def __init__(self, data):
        self.data = data
        self.nameOfModel = "Kadlec PkC SSF"
        self.k_Const = -1
        self.background_Const = -1

    def area(self):
        x = (self.influentQuality-self.backgroundEffluentQuality)/(selfnecessaryEffluentQuality-self.backgroundEffluentQuality)  
        metersCubed = ((self.cells*self.flowRate)*((x)**(1/cells) - 1))/self.k_Const
        return metersCubed


    def effluent(self):        
        numerator = self.influentQuality - self.backgroundEffluentQuality
        denominator = (1+(self.k_Const/(self.cells*(self.flowRate/self.area))))**self.cells
        return numerator/denominator + self.backgroundEffluentQuality



class KadlecSSF_BOD(KadlecSSF):
    def __init__(self, data, k=None):
        if k is None:
            self.k_Const = 76/365
        else:
            self.k_Const = k

        self.cells = data.numberOfCells
        self.area = data.area
        self.flowRate = data.avgFlowRate
        self.influentQuality = data.influentQuality['BOD']
        self.backgroundEffluentQuality = data.backgroundEffluentQuality['BOD']
























'''

class Wetland():

    def __init__(self, site):
        self.site = site
        self.kadlecSSF = KadlecSSF(site)
        self.output = PresentData(site)
        

        self.model = self.kadlecSSF

        self.wetlandType = 'SSF'
            
    def changeWetlandType(self, newType):
        self.wetlandType = newType            

    #Area Calls
    def area(self, qualityType, cells=None, k=None, c_i=None):
        if cells is None:
            cells = self.site.numberOfCells
        if k is None:
            k = self.model.k_Const[qualityType]
        if c_i is None:
            c_i=self.site.currentSepticTankEffluent[qualityType]

        return self.model.area(qualityType, cells=cells, k=k, c_i=c_i)
        
    def printArea(self, qualityType, cells=None, k=None, c_i=None):
        if cells is None:
            cells = self.site.numberOfCells
        if k is None:
            k = self.model.k_Const[qualityType]
        if c_i is None:
            c_i=self.site.currentSepticTankEffluent[qualityType]

        print("The %s Bed Area (m^2): %f" % (self.model.nameOfModel, self.model.area(qualityType, cells=cells, k=k, c_i=c_i)))
        
    
    #Effluent Calls   
    def effluent(self, qualityType, cells=None, area=None, k=None):
        if cells is None:
            cells = self.site.numberOfCells
        if area is None:
            area = self.site.area
        if k is None:
            k = self.model.k_Const[qualityType]

        return self.model.effluent(qualityType, cells=cells, area=area, k=k)
        
    def printEffluent(self, qualityType, cells=None, area=None, k=None):
        if cells is None:
            cells = self.site.numberOfCells
        if area is None:
            area = self.site.area
        if k is None:
            k = self.model.k_Const[qualityType]

        print("The %s Bed Effluent (m^2): %f" % (self.model.nameOfModel,self.model.effluent(qualityType, cells=cells, area=area, k=k)))
        
    #Print Graphs
    def printChangingWaterQualityGraph(self, qualityType, highlightedValues=None):
        if highlightedValues is None:
            
            highlightedValues = [155,286] #EPA high and low
         
        self.output.printWaterQualityGraph(self.model, qualityType, self.model.site.necessaryEffluentQuality[qualityType], 1500, highlightedValues)
    
    def printChangingAreaGraph(self):
        largestArea = int(self.area('BOD')) 
        self.output.printChangingAreaGraph(self.model,  15, largestArea)
        return

    #Print table of Results
    def printTableOfEffluents(self):
        tempArea = self.site.area
        self.site.area = self.area('BOD')
        table = [['Effluent Calculations', ' ', ' '],
                 ['Area: ', round(self.site.area, 2), ' ', ' '],
                 ['Quality Type', 'Input Effluent', 'Background Effluent', 'Output Effluent']]

        for qualityType in self.kadlecSSF.worksFor:
            table.append([qualityType, 
                         round(self.site.currentSepticTankEffluent[qualityType], 2), 
                         round(self.site.backgroundEffluent[qualityType], 2), 
                         round(self.effluent(qualityType), 2)])
        
        self.site.area = tempArea

        print(tabulate.tabulate(table, tablefmt="simple"))

    def printTableOfAreaCalcs(self, qualityType, k=None):
        self.output.printTableOfCalcs('BOD', self.model)

        
    def printPDFTableOfCalcs(self, qualityType, filename=None, k=None):
        if k is None:
            k = self.model.k_Const[qualityType]
        
        if filename is None:
            filename = qualityType + "Calcs"
            self.output.printTableOfCalcs('BOD', self.model, filename=filname)
        else:
            self.output.printTableOfCalcs('BOD', self.model, filename=filename)

    def printCurrentInputs(self):
        table = [["Site: ", self.site.name, " ", " "],
                 ["Water Quality", " ", " ", " "],
                 ["Quality Type", "Input Effluent", "Output Effluent", "Background Effluent"]]
        
        count = 3
        for qualityType in self.site.currentSepticTankEffluent:
            table.append([])
            table[count].append(qualityType + ": ")
            table[count].append(round(self.site.currentSepticTankEffluent[qualityType], 2))
            table[count].append(round(self.site.necessaryEffluentQuality[qualityType], 2))
            table[count].append(round(self.site.backgroundEffluent[qualityType], 2))
            count +=1

        table.append([" ", " ", " ", " "])
        table.append(["Design Values", " ", " ", " "])
        table.append(["Water Temp: ", self.site.waterTemp, "C", " "])
        table.append(["Flow Rate: ", self.site.avgFlowRate, "m^3/day", " "])
        table.append(["Number of Cells: ", self.site.numberOfCells, " ", " "])
        table.append(["Porosity: ", self.site.porosity, " ", " "])
        table.append(["Depth: ", self.site.depth, "m", " "])
        table.append(["Area: ", self.site.area, "m^2", " "])
        table.append(["Tank Area: ", self.site.tankArea, "m^2", " "])
        

        print(tabulate.tabulate(table, tablefmt="simple"))




#Virtual Class of the Kadlec Models
class Kadlec():

    #Volumetric Design Equations
    def backgroundConcentration(self, qualityType): 
        return (self.background_Const[qualityType]*self.theta_Const[qualityType]**(self.site.waterTemp-20))
      
    def isEffluentQualityTooLow(self, qualityType):
        if self.backgroundConcentration(qualityType) > self.site.necessaryEffluentQuality[qualityType]:
            isEffluentTooLow = True
        else: 
            isEffluentTooLow = False   
        return isEffluentTooLow
    
    
    def safeFunctionCall(self, function, qualityType):
        if self.isEffluentQualityTooLow(qualityType):
            print("Your effluent %s requirements are too low for this %s influent value (%.2f vs %.2f). Change area or C_in" % (qualityType, qualityType, self.site.necessaryEffluentQuality[qualityType], self.backgroundConcentration(qualityType)))
            return 0
        else:
            if function == 'area':
                return self.area(qualityType)
            else:
                return self.effluent(qualityType)
    

    def minNecessaryEffluentQuality(self):
        listOfMinValues = []
        for qualityType in self.background_Const:
            listOfMinValues.append(self.background_Const[qualityType])  
        return listOfMinValues




class KadlecSSF_Old(Kadlec):

    def __init__(self, site):
        self.site = site

        self.k_Const = {'BOD':76/365, 
                        'organicNitrogen':19.6/365, 
                        'ammonia':11.4/365, 
                        'nitrate':42/365, 
                        'totalNitrogen':9.1/365, 
                        'fecalColiform':103/365,
                        'TSS':0.22} 

        self.theta_Const =      {'BOD':1.0, 
                                 'TSS':1.0, 
                                 'organicNitrogen':1.05, 
                                 'ammonia':1.04, 
                                 'nitrate':1.09, 
                                 'totalNitrogen':1.05, 
                                 'totalPhosphorus':1, 
                                 'fecalColiform':1}

        self.background_Const = {'BOD':8}
        

        self.worksFor = ['BOD',
                        'TSS',
                        'organicNitrogen', 
                        'ammonia', 
                        'nitrate', 
                        'totalNitrogen', 
                        'fecalColiform']

        self.nameOfModel = "Kadlec PkC SSF"


    #Volumetric Design Equations
    def area(self, qualityType, cells=None, k=None, c_i=None):   
        if cells is None:
            cells = self.site.numberOfCells
        if k is None:
            k = self.k_Const[qualityType]
        if c_i is None:
            c_i=self.site.currentSepticTankEffluent[qualityType]

        x = (c_i-self.site.backgroundEffluent[qualityType])/(self.site.necessaryEffluentQuality[qualityType]-self.site.backgroundEffluent[qualityType])  
        metersCubed = ((cells*self.site.avgFlowRate)*((x)**(1/cells) - 1))/k
        return metersCubed
      
    def effluent(self, qualityType, cells=None, area=None, k=None):
        if cells is None:
            cells = self.site.numberOfCells
        if area is None:
            area = self.site.area
        if k is None:
            k = self.k_Const[qualityType]

        if qualityType == 'TSS':
            TSSEffluent = 1.5+0.22*self.site.currentSepticTankEffluent[qualityType]
            if TSSEffluent < self.site.backgroundEffluent['TSS']:
                return self.site.backgroundEffluent['TSS']
            else: 
                return TSSEffluent
        else:
            a = (self.site.currentSepticTankEffluent[qualityType] - self.site.backgroundEffluent[qualityType])
            b = (1+(k/(cells*(self.site.avgFlowRate/area))))**cells
            return a/b + self.site.backgroundEffluent[qualityType]










class tables():
    def __init__(self):
        self.tableBODRateConstants = {"**C~i~ (mg/L)**":["**FWS**", "P", "C^\*^, (mg/L)", "30th %ile  (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)", "  ", "**HSSF**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)", " ",  "**VFSF**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)"], 
                    "**BOD Tertiary 0-30 (mg/L)**":[" ",1, 2, 16, 33, 79, " ", " ",3, 1, 36, 86, 224, " ", " ",6,0,22,63,105], 
                    "**BOD Tertiary 30-100 (mg/L)**":[" ",1,5,16,'**41**',67," "," ",3,5,24,'**37**',44, " ", " ",6,0,40,"**56**",79], 
                    "**BOD Tertiary 100-200 (mg/L)**":[" ",1,10,23,'**36**',112," "," ",3,10,15,'**25**',44, " ", " ",6,0,53,"**76**",122], 
                    "**BOD Tertiary >200 (mg/L)**":[" ",1,20,54,189,439," "," ",3,15,21,66,114, " ", " ",6,0,48,71,93]}
            
        self.tableRateConstants = {"**C~i~ (mg/L)**":["**FWS**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)", "  ", "**HSSF**", "P", "C^\*^, (mg/L)", "30th %ile (k, m/yr)", "50th %ile (k, m/yr)", "70th %ile (k, m/yr)"], 
            "**ORG-N**":[" ",3,1.5,10.7,'**17.3**',27.4," "," ",6,1,8.8,'**19.6**',38.0], 
            "**NH~4~-N**":[" ",3,0,8.7,'**14.7**',45.1," "," ",6,0,5.2,'**11.4**',18.8], 
            "**NO~x~-N**":[" ",3,0,18.5,'**26.5**',33.6," "," ",8,0,32,'**42**',73], 
            "**TKN**":[" ",3,1.5,6.1,'**9.8**',13.6," "," ",6,1,4.8,'**9.1**',14.6], 
            "**TN**":[" ",3,1.5,6.6,'**12.6**',24.2," "," ",6,1,4.7,'**8.4**',14.2], 
            "**TP**":[" ",3.4,0.002,4.5,'**10.0**',16.7," "," ","*","*","*","*","*"], 
            "**FC**":[" ",3,40,49,'**83**',177," "," ",6,0,56,'**103**',181]}

        
'''


