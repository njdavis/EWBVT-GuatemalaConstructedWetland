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
            xAxis.append(value) 
            site.currentSepticTankEffluent[waterQualityParameter] = value
            yAxis.append(model.treatmentArea(waterQualityParameter, site))

                 
        for parameterValue in highlightedValuesX:
            site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
            outputSubPlot.annotate('(%d, %d)' % (parameterValue, model.treatmentArea(waterQualityParameter, site)), xy=(parameterValue+30, model.treatmentArea(waterQualityParameter, site)-20 ))

            plt.plot(xAxis, yAxis, '-', parameterValue, model.treatmentArea('BOD', site), 'h') 

        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        outputSubPlot.set(title=r'%s: %s' % (model.nameOfModel, waterQualityParameter),
        xlabel='%s (%s)' % (waterQualityParameter, units), ylabel= 'Area Required for Constructed Wetland $(m^2)$')


        outputPlot.savefig("../Graphs and Charts/%s-%s.pdf" % (model.nameOfModel, waterQualityParameter), bbox_inches='tight')

        site.currentSepticTankEffluent[waterQualityParameter] = tempWaterQuality

    def printMultipleModelsArea(self, models, waterQualityParameter, site, waterQualityLow, waterQualityHigh,  highlightedValuesX):
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
        
        for i, model in enumerate(models):
            yAxis.append([])
            xAxis.append([])
            
            for value in range(waterQualityLow, waterQualityHigh):   
                xAxis[i].append(value) 
                site.currentSepticTankEffluent[waterQualityParameter] = value
                yAxis[i].append(model.treatmentArea(waterQualityParameter, site))
 
            outputSubPlot.plot(xAxis[i], yAxis[i], '-', label = model.nameOfModel) 

            for parameterValue in highlightedValuesX:  
                site.currentSepticTankEffluent[waterQualityParameter] = parameterValue
                outputSubPlot.annotate('(%d, %d)' % (parameterValue, model.treatmentArea(waterQualityParameter, site)), xy=(parameterValue+30, model.treatmentArea(waterQualityParameter, site)-20 ))
                outputSubPlot.plot(parameterValue, model.treatmentArea('BOD', site), 'h')
            

        outputSubPlot.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        units = "mg/L"
        if waterQualityParameter == "fecalColiform":
            units = "cfu/100ml"

        graphTitle = ""
        for model in models:
            graphTitle = graphTitle + model.nameOfModel + " v "
        graphTitle = graphTitle[:-3] + ": " + waterQualityParameter

        outputSubPlot.set(title=graphTitle, xlabel='%s (%s)' % (waterQualityParameter, units), ylabel= 'Area Required for Constructed Wetland $(m^2)$')


        outputPlot.savefig("../Graphs and Charts/%s vs %s-%s.pdf" % (models[0].nameOfModel, models[1].nameOfModel, waterQualityParameter), bbox_inches='tight')

        site.currentSepticTankEffluent[waterQualityParameter] = tempWaterQuality
        

    def printMultipleModelsEffluent(self, model,  site, waterQualityLow, waterQualityHigh,  highlightedValuesX):
        '''
        Prints graphs about how changing certain water quality parameters changes the area needed
        waterQualityParameter=string, site = siteInfo(), waterQualityLow = int, waterQualityHigh = int, highlightedValues = [x,..]
        '''
        tempArea = site.area
        
        waterQualityList = []
        yAxis = []
        xAxis = []
        areaEPA = []

        outputPlot = plt.figure()
        outputSubPlot = outputPlot.add_subplot(111) 
        
        for i, waterQualityParameter in enumerate(model.worksFor):
            yAxis.append([])
            xAxis.append([])
            
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






