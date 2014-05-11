###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################

from os import path
from re import split
#from numpy import *
### Context Class
### Store randome nubmer generator and all variables which define the experiment

### @TODO: Add proper get and set commands to this class

### @TODO: Catch all "KeyError" exceptions and set them to a default value
###        create a default value dictionary to accomplish this

### @TODO: Refactor simulation specific variables into a seperate structer within the simulation interface
###        This class should only specify *which* simulator and simulation config file to use with it

class cContext(object):


    ### Function - context::__init__
    ### Purpose  - Instasiate all member variables and inilize random number seed
    ### Input    - random number seed and path to options file
    ### Output   - inilized context object
    def __init__ (self, randomSeed, optFilePath):

        #intilized the random number generator and seed
        import random
        self.random = random.Random()
        
        self.random.seed(randomSeed)

        #initilize varialbe for the most recent solution ID
        self.currID = 0
        self.currGen = 0

        #get a dictionary of all options in the options file
        self.optDict = self.getOptDict(optFilePath)

        print self.optDict

        self.seedSolution = self.optDict["seedSolution"]
        self.popSize = int(self.optDict["popSize"])
        self.numGen = int(self.optDict["numGen"])
        self.mutRate = float(self.optDict["mutRate"])
        
        

    ###------------------END-------------------------###

    def get(self, s):
        res = None
        try:
            res = self.optDict[s]
            return res
        except KeyError:
            print "WARNING: no value %s in context file." % s
            return res


    def getInt(self, s):
        res = None
        try:
            res = self.optDict[s]
            return int(res)
        except KeyError:
            print "WARNING: no value %s in context file." % s
            return res

    ### Function - context::getOptDict
    ### Purpose  - read in the options file and create a dictionary
    ### Input    - file path
    ### Output   - dictionary contining entries for each simulation option
    def getOptDict(self, filename):

        #@TODO: add support for spaces and comments in the file
        
        #make sure it's there
        if(path.exists(filename)):

            #open the file and dump each line into an array
            fp = open(filename,'r')
            data = fp.readlines()
            fp.close()

            #create a temporary list of tuples to hold dict vals
            vals = []

            #split each line, strip the white space and append as a tuple
            for line in data:
                temp = split(':',line)
                vals.append((temp[0].strip(), temp[1].strip()))
            
            #return the dictionary of command line options
            return dict(vals)

        #Otherwise, the user fails at life 
        else:
            print "ERROR: unable to find file: " +  filename + "\n"
            quit()
    ###------------------END-------------------------###

    ### Function - context::getID
    ### Purpose  - get a new ID for a solution object -- increment ID count
    ### Input    - none
    ### Output   - new integer representing the ID of the solution
    def getID (self):
        self.currID = self.currID + 1
        return self.currID
    ###------------------END-------------------------###

    ### Function - context::getGen
    ### Purpose  - get the current generation
    ### Input    - none
    ### Output   - int of the current generation
    def getGen (self):
        return self.currGen
    ###------------------END-------------------------###
