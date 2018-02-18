import matplotlib.pyplot as plt
from siteInfo import Site
import tabulate, copy, os, sys


class PresentData(): 

    def __init__(self, site):
        self.site = site

    def printWaterQualityGraph(self, model, waterQualityParameter,  waterQualityLow, waterQualityHigh,  highlightedValuesX):
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

        
        areaCurve = plt.plot(xAxis, yAxis, '-')

        for parameterValue in highlightedValuesX:
            model.site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            if model.nameOfModel == "Kadlec kC SSF":
                area = model.safeFunctionCall('area', waterQualityParameter)
            else:
                area = model.area(waterQualityParameter)

            model.site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            
            outputSubPlot.annotate('(%d, %d)' % (parameterValue, area), xy=(parameterValue+30, area-19 ))
            plt.plot(parameterValue,area, 'h')

        
        
            

        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        legendString = '%s Output Value = %0.2f (mg/L)\nFlow Rate = %0.2f ($m^3$/d)\nNumber of Cells%0.2f' % (waterQualityParameter, model.site.necessaryEffluentQuality[waterQualityParameter], model.site.avgFlowRate, model.site.numberOfCells) 
        if model.nameOfModel.startswith("Kadlec P"): 
            legendString = legendString + ("\nk = %0.4f" % model.k_Const[waterQualityParameter])
        elif model.nameOfModel.startswith("Kadlec k"):
            legendString = legendString + ("\nk = %d" % model.k_Const[waterQualityParameter])

        outputPlot.legend(areaCurve, (legendString,), loc='center right')

        outputSubPlot.set(title=('%s: %s' % (model.nameOfModel, waterQualityParameter)),
        xlabel='%s (%s) ' % (waterQualityParameter, units, ), ylabel= 'Area Required for Constructed Wetland $(m^2)$')

        folderLocation = os.path.join(sys.path[0], "../visualization/%s-%s.pdf" % (model.nameOfModel, waterQualityParameter))
        outputPlot.savefig(folderLocation, bbox_inches='tight')

        model.site.currentSepticTankEffluent[waterQualityParameter] = tempWaterQuality

            

    def printChangingAreaGraph(self, model,  waterQualityLow, waterQualityHigh):
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

        
        outputSubPlot.set(title=('%s: Effluent Quality' % (model.nameOfModel)), xlabel= 'Area Required for Constructed Wetland $(m^3)$', ylabel=units)

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
        text_file.write(tabulate.tabulate(self.SSFModelParmaters, headers="keys", tablefmt="gid"))
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

    def printInfoAboutFunctions(self, functions, purpose, inputOptionsList):
        
        table = []
        for index, functionValue in enumerate(functions):
            table.append(["**Function:** ", functionValue, " "])
            table.append(["**Purpose:**", purpose[index]])
            table.append(["**Inputs**", "**Input Options**"])
        
            for columns in inputOptionsList[index]:
                row = []
                for value in columns:
                    row.append(value)

                table.append(row)
            table.append([" ", " "])
            table.append([" ", " "])


        folderLocation = os.path.join(sys.path[0], "../visualization/charts/functions.txt")

        text_file = open(folderLocation, "w")
        text_file.write(tabulate.tabulate(table, tablefmt="grid"))
        text_file.close()

        

    def printTableOfCalcs(self, qualityType, model, k=None, filename=None):
        if k is None:
            k = model.k_Const[qualityType]
        else:
            model.k_Const[qualityType] = k
        if filename is None:
            noFile = True
        else:
            noFile = False
   
        self.site.tankArea = self.site.area/4
        self.site.numberOfCells = 4
        tankHLR = self.site.avgFlowRate/self.site.tankArea
        HLR = (self.site.avgFlowRate/self.site.area)

        temp = self.site.currentSepticTankEffluent['BOD']
        effl1 = model.effluent('BOD', cells=1, area=self.site.tankArea, k=k)
        self.site.currentSepticTankEffluent['BOD'] = effl1
        effl2 = model.effluent('BOD', cells=1, area=self.site.tankArea, k=k)
        self.site.currentSepticTankEffluent['BOD'] = effl2
        effl3 = model.effluent('BOD', cells=1, area=self.site.tankArea, k=k)
        self.site.currentSepticTankEffluent['BOD'] = effl3
        effl4 = model.effluent('BOD', cells=1, area=self.site.tankArea, k=k)
        self.site.currentSepticTankEffluent['BOD'] = effl4
        self.site.currentSepticTankEffluent['BOD'] = temp 

        efflTotal = round(model.effluent('BOD', cells=4, area=self.site.area, k=k), 2)
        
        c_i = self.site.currentSepticTankEffluent[qualityType]
        c_star = self.site.backgroundEffluent[qualityType]
        flow = self.site.avgFlowRate

        tabulate.PRESERVE_WHITESPACE = True

        table = [['**Input Parameters**'  ,'   '                   ,'   '        ,'   ','   ', '   ', '   ', '   '], 
                ['Flow rate, Q:'                      , self.site.avgFlowRate  ,'(m^3^/d)'     ,'   ','   ', '   ', '   ', '   '],
                ['Cells, P:'                            , self.site.numberOfCells,'(system)'     ,'   ','   ', '   ', '   ', '   '],
                ['Area, A:'                           , self.site.area         ,'(m^2^)'       ,'   ','   ', '   ', '   ', '   '],
                ['Cell Area:'                         ,round(self.site.area/4, 2), '(m^3^)'    ,'   ','   ', '   ', '   ', '   '],
                ['C~i~:'                              , c_i                    ,'(mg/L)'       ,'   ','   ', '   ', '   ', '   '],
                ['C*:'                                , c_star                 ,'(mg/L)'       ,'   ','   ', '   ', '   ', '   '],
                ['k:'                                 , round(k*365, 2)        ,'(m/yr)'       ,'   ','   ', '   ', '   ', '   '],
                ['k:'                                 , round(k, 3)            ,'(m/d)'        ,'   ','   ', '   ', '   ', '   '], 
                ['   '                  , '   '                  ,'   '       ,'   ','   '],
            ['**Calculated Values**','   ' ,'**System In**','**Exit Cell 1**','**Exit Cell 2**','**Exit Cell 3**','**Exit Cell 4**','**System Out**'],
            ['Net flow'             ,'(m^3^/d)', flow        ,flow             , flow            ,  flow           , flow            , flow           ],
            ['HLR, q'               ,'(m/d)'   ,round(HLR, 2),round(tankHLR, 2),round(tankHLR, 2),round(tankHLR, 2),round(tankHLR, 2), round(HLR, 2)  ],
            ['Concentration'        ,'(mg/L)'  ,c_i          ,round(effl1, 2)  ,round(effl2, 2)  ,round(effl3, 2)  ,round(effl4, 2)  , efflTotal      ],
            ['HRT'                  ,'(days)'  ,'N/A'        ,'N/A'            ,'N/A'            ,'N/A'            ,'N/A'            ,'N/A'           ]]

        if noFile is False:
            folderLocation = os.path.join(sys.path[0], "../visualization/charts/%s.txt" % filename)

            text_file = open(folderLocation, "w")
            text_file.write(tabulate.tabulate(table, tablefmt="grid"))
            text_file.write("\n \nTable: Calculations from Kadlec Second Edition {#tbl:PkCCaluculated}")
            text_file.close()
        else:
            print(tabulate.tabulate(table, tablefmt="simple"))
        






