import matplotlib.pyplot as plt

class PresentData():

    def printAreaGraph(self, model, waterQualityParameter, site, waterQualityLow, waterQualityHigh,  highlightedValuesX):
        '''
        Prints graphs about how changing certain water quality parameters changes the area needed
        waterQualityParameter=string, site = siteInfo(), waterQualityLow = int, waterQualityHigh = int, highlightedValues = [x,..]
        '''

        tempWaterQuality = site.currentSepticTankEffluent[waterQualityParameter] 
        waterQualityList = []
        yAxis = []
        xAxis = []
        areaEPA = []

        outputPlot = plt.figure()
        outputSubPlot = outputPlot.add_subplot(111)
        
        for value in range(waterQualityLow, waterQualityHigh):
            
            site.currentSepticTankEffluent[waterQualityParameter] = value
            if model.nameOfModel == "Kadlec Subsurface Flow":
                yValue = model.safeFunctionCall('area', waterQualityParameter, site)
            else:
                yValue = model.treatmentArea(waterQualityParameter, site)

            if yValue != 0:
                xAxis.append(value) 
                yAxis.append(yValue)

                 
        for parameterValue in highlightedValuesX:
            site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            if model.nameOfModel == "Kadlec Subsurface Flow":
                area = model.safeFunctionCall('area', waterQualityParameter, site)
            else:
                area = model.treatmentArea(waterQualityParameter, site)

            site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            outputSubPlot.annotate('(%d, %d)' % (parameterValue, area), xy=(parameterValue+30, area-19 ))

            plt.plot(xAxis, yAxis, '-', parameterValue,area, 'h') 

        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        outputSubPlot.set(title=r'%s: %s' % (model.nameOfModel, waterQualityParameter),
        xlabel='%s (%s)' % (waterQualityParameter, units), ylabel= 'Area Required for Constructed Wetland $(m^2)$')


        outputPlot.savefig("../Graphs and Charts/%s-%s.pdf" % (model.nameOfModel, waterQualityParameter), bbox_inches='tight')

        site.currentSepticTankEffluent[waterQualityParameter] = tempWaterQuality

            

    def printMultipleModelsArea(self, model,  site, waterQualityLow, waterQualityHigh,  highlightedValuesX):
        '''
        Prints graphs about how changing certain water quality parameters changes the area needed
        waterQualityParameter=string, site = siteInfo(), waterQualityLow = int, waterQualityHigh = int, highlightedValues = [x,..]
        '''
        tempArea = site.area
        
        waterQualityList = []
        yAxis = []
        xAxis = []
        listOfAreas = []
        areaEPA = []

        outputPlot = plt.figure()
        outputSubPlot = outputPlot.add_subplot(111) 
        

        for i, waterQualityParameter in enumerate(model.worksFor):
            yAxis.append([])
            xAxis.append([])
            
            #Kadlec Model has conditions that can report impossible values
            if model.nameOfModel == "Kadlec Subsurface Flow":
                if model.isEffluentQualityTooLow(waterQualityParameter, site):
                    outputSubPlot.set(title=('Your Effluent requirements are Too Low: !< %.2f' % model.backgroundConcentration(waterQualityParameter, site)), xlabel= 'Your Effluent requirements are Too Low', ylabel='Your Effluent requirements are Too Low')
                    outputPlot.savefig("../Graphs and Charts/%s Effluent.pdf" % (model.nameOfModel), bbox_inches='tight')

                    return 
                else:                        
                    for value in range(waterQualityLow, waterQualityHigh):   
                        xAxis[i].append(value) 
                        site.area = value
                        yAxis[i].append(model.safeFunctionCall('effluent', waterQualityParameter, site))
            else: 
                for value in range(waterQualityLow, waterQualityHigh):   
                    xAxis[i].append(value) 
                    site.area = value
                    yAxis[i].append(model.effluent(waterQualityParameter, site))

            outputSubPlot.plot(xAxis[i], yAxis[i], '-', label = waterQualityParameter) 
        
        outputSubPlot.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        graphTitle = model.nameOfModel + ":"
        for waterQualityParameter in model.worksFor:
            graphTitle = graphTitle + " " + waterQualityParameter + " V"
        graphTitle = graphTitle[:-3] 

        outputSubPlot.set(title=graphTitle, xlabel= 'Area Required for Constructed Wetland $(m^2)$', ylabel=units)

        outputPlot.savefig("../Graphs and Charts/%s Effluent.pdf" % (model.nameOfModel), bbox_inches='tight')

        site.area = tempArea






