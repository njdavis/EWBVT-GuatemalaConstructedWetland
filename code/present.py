import matplotlib.pyplot as plt
from wetlandCalc import ReedSubsurfaceFlow, ReedFreewaterFlow, KadlecSubsurfaceFlow
from siteInfo import Site
import tabulate, copy, os, sys


class PresentData(): 

    def printAreaGraph(self, model, waterQualityParameter,  waterQualityLow, waterQualityHigh,  highlightedValuesX):
        '''
        Prints graphs about how changing certain water quality parameters changes the area needed
        waterQualityParameter=string, site = siteInfo(), waterQualityLow = int, waterQualityHigh = int, highlightedValues = [x,..]
        '''

        tempWaterQuality = model.site.currentSepticTankEffluent[waterQualityParameter] 
        waterQualityList = []
        yAxis = []
        xAxis = []
        areaEPA = []

        outputPlot = plt.figure()
        outputSubPlot = outputPlot.add_subplot(111)
        
        for value in range(waterQualityLow, waterQualityHigh):
            
            model.site.currentSepticTankEffluent[waterQualityParameter] = value
            if model.nameOfModel == "Kadlec Subsurface Flow":
                yValue = model.safeFunctionCall('area', waterQualityParameter)
            else:
                yValue = model.area(waterQualityParameter)

            if yValue != 0:
                xAxis.append(value) 
                yAxis.append(yValue)

                 
        for parameterValue in highlightedValuesX:
            model.site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            if model.nameOfModel == "Kadlec Subsurface Flow":
                area = model.safeFunctionCall('area', waterQualityParameter)
            else:
                area = model.area(waterQualityParameter)

            model.site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            outputSubPlot.annotate('(%d, %d)' % (parameterValue, area), xy=(parameterValue+30, area-19 ))

            plt.plot(xAxis, yAxis, '-', parameterValue,area, 'h') 

        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        outputSubPlot.set(title=r'%s: %s' % (model.nameOfModel, waterQualityParameter),
        xlabel='%s (%s)' % (waterQualityParameter, units), ylabel= 'Area Required for Constructed Wetland $(m^2)$')

        folderLocation = os.path.join(sys.path[0], "../visualization/%s-%s.pdf" % (model.nameOfModel, waterQualityParameter))
        outputPlot.savefig(folderLocation, bbox_inches='tight')

        model.site.currentSepticTankEffluent[waterQualityParameter] = tempWaterQuality

            

    def printMultipleModelsArea(self, model,  waterQualityLow, waterQualityHigh,  highlightedValuesX):
        '''
        Prints graphs about how changing certain water quality parameters changes the area needed
        waterQualityParameter=string, site = siteInfo(), waterQualityLow = int, waterQualityHigh = int, highlightedValues = [x,..]
        '''
        tempArea = model.site.area
        
        waterQualityList = []
        yAxis = []
        xAxis = []
        listOfAreas = []
        areaEPA = []

        outputPlot = plt.figure()
        outputSubPlot = outputPlot.add_subplot(111) 
        
        worksFor = model.worksFor[:-1]
        for i, waterQualityParameter in enumerate(worksFor):
            yAxis.append([])
            xAxis.append([])
            
            #Kadlec Model has conditions that can report impossible values
            if model.nameOfModel == "Kadlec Subsurface Flow":
                if model.isEffluentQualityTooLow(waterQualityParameter):
                    outputSubPlot.set(title=('Your Effluent requirements are Too Low: !< %.2f' % model.backgroundConcentration(waterQualityParameter, site)), xlabel= 'Your Effluent requirements are Too Low', ylabel='Your Effluent requirements are Too Low')
                    outputPlot.savefig("../visualization/%s Effluent.pdf" % (model.nameOfModel), bbox_inches='tight')

                    return 
                else:                        
                    for value in range(waterQualityLow, waterQualityHigh):   
                        xAxis[i].append(value) 
                        model.site.area = value
                        yAxis[i].append(model.safeFunctionCall('effluent', waterQualityParameter))
            else: 
                for value in range(waterQualityLow, waterQualityHigh):   
                    xAxis[i].append(value) 
                    model.site.area = value
                    yAxis[i].append(model.effluent(waterQualityParameter))

            outputSubPlot.plot(xAxis[i], yAxis[i], '-', label = waterQualityParameter) 
        
        outputSubPlot.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        graphTitle = model.nameOfModel + ":"
        for waterQualityParameter in model.worksFor:
            graphTitle = graphTitle + " " + waterQualityParameter + " V"
        graphTitle = graphTitle[:-3] 

        outputSubPlot.set( xlabel= 'Area Required for Constructed Wetland $(m^2)$', ylabel=units)

        folderLocation = os.path.join(sys.path[0], "../visualization/%s Effluent.pdf" % (model.nameOfModel))
        
        outputPlot.savefig(folderLocation, bbox_inches='tight')

        model.site.area = tempArea

    def convertKadlecSSFBackground_Const(self, model):
        out = copy.deepcopy(model.background_Const)
        for value in model.worksFor:
            if value == 'BOD':
                out[value] = "3.5+0.053 C~i~"
            if value == 'TSS':
                out[value] = "7.8+0.063 C~i~" 
                
        return out

    def table21_1(self, model):
        convBackground_Const = self.convertKadlecSSFBackground_Const(model)
        out = []
        for x, qualityType in enumerate(model.worksFor):
            out.append([])
            out[x].append(str(model.k_Const[qualityType]))
            out[x].append(str(model.theta_Const[qualityType]))
            out[x].append(convBackground_Const[qualityType])

        return out
    
    def printTable21_1(self, model):
        values = self.table21_1(model)
        #from table 21-1: S
        #SF Model Parameter Values -- Preliminary
        self.SSFModelParmaters = {"": ["k20, m/yr", "$\Theta$", "C*, mg/L"], "BOD":values[0], "TSS":values[1], "Organic N":values[2], 'NH~4~-N':values[3] , 'NO~x~N':values[4], 'TN':values[5], 'TP':values[6], 'FC':values[7]}

        folderLocation = os.path.join(sys.path[0], "../visualization/charts/Kadlec 21-1 Table.txt")
        
        text_file = open(folderLocation, "w")
        text_file.write(tabulate.tabulate(self.SSFModelParmaters, headers="keys", tablefmt="grid"))
        text_file.write("\n \nTable: Typical Media Characteristics for Subsurface Flow Wetlands {#tbl:MediaCharacteristicsReed}")
        text_file.close()

    def printTableOfEffluent(self, model, listOfAreas):
        values = []
        for typeCount, qualityType in enumerate(model.worksFor):
            values.append([])
            for area in listOfAreas:
                model.site.area = area
                effluent = model.effluent(qualityType)
                if type(effluent) is str:
                    print("Your effluent %s requirements are too low for this %s influent value (%.2f vs %.2f). Change area or C_in" % (qualityType, qualityType, model.site.necessaryEffluentQuality[qualityType], model.site.backgroundConcentration(qualityType)))
                    values[typeCount].append("N/A")
                else:
                    values[typeCount].append("%.2f" % effluent)

        self.SSFModelParmaters = {"Area (m^2^":listOfAreas, "BOD":values[0], "TSS":values[1], "Organic N":values[2], 'NH~4~-N':values[3] , 'NO~x~N':values[4], 'TN':values[5], 'TP':values[6], 'FC':values[7]}

        folderLocation = os.path.join(sys.path[0], "../visualization/charts/Kadlec Effluent with Areas [%s].txt" % ', '.join(map(str, listOfAreas)))

        text_file = open(folderLocation, "w")
        text_file.write(tabulate.tabulate(self.SSFModelParmaters, headers="keys", tablefmt="grid"))
        text_file.write("\n \nTable: Possible Effluent Values at Certain Areas {#tbl:specificAreas}")
        text_file.close()

    
    def printTable(self, filename, inputDict, title=''):
        tempDict = {}
        checkIfList = []
        for header in inputDict:
            if (type(inputDict[header])) != type(checkIfList): 
                tempList = [0]
                tempList[0] = inputDict[header] 
                tempDict[header] = tempList
            else: 
                tempDict = inputDict

                
        folderLocation = os.path.join(sys.path[0], "../visualization/charts/%s.txt" % filename)

        text_file = open(folderLocation, "w")
        text_file.write(tabulate.tabulate(tempDict, headers="keys", tablefmt="grid"))
        text_file.write(" \n \n Table: %s {#tbl:%s}" % (title, filename))
        text_file.close()







