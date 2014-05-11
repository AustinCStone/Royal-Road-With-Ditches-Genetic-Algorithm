###############################
## Python Evolution - v 0.1  ##                        
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################


### Stats Class
### A simple container class to store summary statisitics for each generation of evolution

###@TODO Make this a dynamic class, have the population create columns

class cStats(object):


    ### Function - cPopulation::__init__
    ### Purpose  - Instasiate a new stats object
    ### Input    - None
    ### Output   - None
    def __init__(self):

        #A simple calculation for 
        self.__currGen = 0

        #container for an array of dictionaries containing stats
        self.__statsArray = []

    ### Function - cPopulation::__str__
    ### Purpose  - Get a string continaing all summary statistics
    ### Input    - None
    ### Output   - String
    def __str__(self):
        output = ""

        #I wounder if we actually have anything to write out?
        if len(self.__statsArray) > 0:

            #grab the headers from the first row, these will be the headers in the output string
            header = self.__statsArray[0].viewkeys()

            #isaac suggested this, but I haven't gotten it to work
            #output = ",".join(header)
            
            for column in header:
                output = output + "%s " % column

            #append a newline
            output = output + "\n"

            #for each row, display each column in the correct order
            for d in self.__statsArray:
                for key in header:
                    output = output + "%s " % d[key]
                output = output + "\n"
                

        return output

    ### Function - cPopulation::addGenStats
    ### Purpose  - Add statistics for this generation
    ### Input    - Avg Fit, Max Fit, number of births, number of mutations
    ### Output   - none
    def addGenStats(self, averageFit = None, maxFit = None, nBirths = None, nMuts = None, maxID = None):

        #increment the generation
        self.__currGen = self.__currGen + 1

        #temporary dictionary to hold this generations stats
        newGenStats = {'gen': self.__currGen, 'avgFit': None, 'maxFit': None, 'nBirths': None, 'nMuts': None, 'maxID': None}

        #get the avg fit and other variables
        if(averageFit is not None):
            newGenStats["avgFit"] = float(averageFit)

        if(maxFit is not None):
            newGenStats["maxFit"] = float(maxFit)
        
        if(nBirths is not None):
            newGenStats["nBirths"] = int(nBirths)
            
        if(nMuts is not None):
            newGenStats["nMuts"] = int(nMuts)
            
        if(maxID is not None):
            newGenStats["maxID"] = int(maxID)

        #add the new stats to the array
        self.__statsArray.append(newGenStats)        
        
        return None
