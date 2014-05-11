###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################

import subprocess

from subprocess import Popen
from os import path
from math import floor

from cSolution import *
from cPE_Exceptions import *
from cStats import *

### Population Class
### Polution base class -- Constructs and stores the popuation, handles the selection of each new generation

### This population class uses a simple rank based selection algorithm

class cPopulation(object):


    ### Function - cPopulation::__init__
    ### Purpose  - Instasiate a solution object from the context file--ie the seed solution
    ### Input    - Must take a context object, simulator, and either a seed organism or a copyPopulation
    ### Output   - a new cPopulation object
    def __init__ (self, ctx, simulator, seedOrg=None,copyPopulation=None):

        #we need exactly one of these things, if they are both null or both assigned raise an exception
        if((seedOrg is None and copyPopulation is None) or (seedOrg is not None and copyPopulation is not None)):
            raise(PE_PopulationParameters(""))

        #initalize some variables
        self.__ctx = ctx

        #initiate a stats object to keep track of pertientant information for each generation
        self.__stats = cStats()

        #set the population size
        self.__size = ctx.popSize

        #get a simulator
        self.__sim = simulator

        #array to hold the current population
        self.__population = []

        #store the old generations
        self.__oldPopulationLog = []

        #number of paritions for rank based selection
        self.__partions = 4

        #size of each partion for the rank based selection
        self.__partionSize = self.__ctx.popSize / self.__partions

        #either create a population form a seed organism or copy an exisiting population
        if(seedOrg is not None):
            self.__instansiatePopulationFromOrg(seedOrg)

        if(copyPopulation is not None):
            self.__deepCopyPopulation(copyPopulation)

        #when we are done creating it the population array should always be sorted
        #subsequent populations that are the result of selection should also be sorted
        self.__population.sort()

        #Push the last generation into the genebank
        self.__backupGen()


    ### Function - cSolution::__str__
    ### Purpose  - return an "informal" string representation
    ### Input    - none
    ### Output   - string containing a list of the orgs sepereated by newlines
    def __str__ (self):
        output = ""

        for org in self.__population:
            output = output + str(org) + "\n"

        return output

    
    ### Function - cPopulation::step
    ### Purpose  - advance the simulation one generation
    ### Input    - None
    ### Output   - New generation number
    ### @TODO    - refactor summary statstics into a private helper function
    def step(self):

        #create a new population
        newPopulation = []

        #total fitness
        totalFit = 0

        #max fitness and ID
        maxFitness = float('-inf')
        maxID = None

        #count of births
        count = 0

        #mut count
        nMutations = 0

        #increment the generation count
        self.__ctx.currGen = self.__ctx.currGen + 1

        #fill the population with the appropriate number of orgs
        for x in range(1,self.__ctx.popSize+1):

            #return a copy of a lucky parent
            newOrg = self.__select(x)

            count = count + 1
        
            #check to see if we mutate
            if(self.__ctx.mutRate < self.__ctx.random.random()):
                #mutate
                self.__sim.mutateAndEvaluateOrgFitness(self.__ctx, newOrg)
                
            else:
                #no need to mutate
                #still need to evaluate to set the generation number
                self.__sim.evaluateOrgFitness(self.__ctx, newOrg)
                nMutations = nMutations + 1

            totalFit = totalFit + newOrg.getFitness()

            if(newOrg.getFitness() > maxFitness):
                maxFitness = newOrg.getFitness()
                maxID = newOrg.getID()

            #append the new org to the population
            newPopulation.append(newOrg)

        self.__stats.addGenStats(averageFit = float(totalFit/count), maxFit = maxFitness, maxID = maxID, nBirths = count, nMuts = nMutations)
            
        #make sure the new list is sorted
        newPopulation.sort()

        #push the old generation to the genebank
        self.__backupGen()

        #add the old population to the log
        #self.__oldPopulationLog.append(self.__population)

        #finaly, assign the new population 
        self.__population = newPopulation

        #return the current generation number for shits and giggles
        return self.__ctx.currGen

    ### Function - cPopulation::__select
    ### Purpose  - perform selection on the population
    ### Input    - None
    ### Output   - index of selected organism
    def __select(self, round):

        while True:
            #define possible range for this round of selection
            max = self.__ctx.popSize-1

            #compute the min
            min = self.__partionSize * floor((self.__ctx.popSize - round) / self.__partionSize)

            #grab an appropriate index
            i = self.__ctx.random.randint(min,max)

            print "In round %s, choose %s from %s and %s" % (round, i, max, min)

            if(self.__population[i].getFitness() == float("-inf") or self.__population[i].getFitness() == float("inf")):
                print "Org has leathal mutation, trying again"
            else:
                break

        #return a new solution
        return cSolution(self.__ctx, self.__population[i])

    ### Function - cPopulation::__instansiatePopulationFromOrg
    ### Purpose  - instansiate a new population from a single seed organism
    ### Input    - seed organism
    ### Output   - None, assigns the new organisms to self.__population
    ### @TODO    - Refactor this into two versions with and without the job manager
    def __instansiatePopulationFromOrg(self,seed):

        #initialize the fitness of the seed organism
        self.__sim.evaluateOrgFitness(self.__ctx,seed)

        print seed.getFilename()

        #this is the first generation, so we set the generation number to 1
        #we wait to do this here so that the seed org has generation 0
        self.__ctx.currGen = 1

        #initialize and evalutate a popualtion of mutants
        for x in range(0,self.__size):

            #create a new org
            newOrg = cSolution(self.__ctx, seed)
            
            #check to see if we mutate
            if(self.__ctx.mutRate < self.__ctx.random.random()):
                #mutate
                self.__sim.mutateAndEvaluateOrgFitness(self.__ctx,newOrg)
                
            else:
                #no need to mutate
                #still need to evaluate to set the generation number
                self.__sim.evaluateOrgFitness(self.__ctx,newOrg)
                
            #tack on the new mutator
            self.__population.append(newOrg)
                
        return None

    ### Function - cPopulation::__deepCopyPopulation
    ### Purpose  - create a new population by performing a deep copy of a previous population
    ### Input    - a population to copy
    ### Output   - None, assigns the new organisms to self.__population
    def __deepCopyPopulation(self,copyPopulation):
        return None

    ### Function - cPopulation::dumpSummaryStats
    ### Purpose  - Dump the summary stats for the population so far
    ### Input    - None
    ### Output   - a string containing all summary stats
    def dumpSummaryStats(self):
        return str(self.__stats)


    ### @TODO: all of this functionality, except creating the genebank, should be pushed elsewhere, probably the simulation class
    ### Function - cPopulation::__backupGen
    ### Purpose  - Backup the last generation to the genebank directory
    ### Input    - none, use the context object member class
    ### Output   - none
    def __backupGen(self):

        #path to the genebank
        bankPath = self.__ctx.genebankPath

        #last generation computed
        lastGen  = self.__ctx.currGen - 1

        #command to copy the solution files
        command = "mv gen_%s-* %s/." % (lastGen,bankPath)

        #make sure the target exists; should be executed only once per run
        if( not path.exists(bankPath)):
            Popen(["mkdir %s" % bankPath],shell=True).wait()

        #@TODO: cath the OSError exception in the event that the last generation is not found
        #through your own error instead
        Popen([command],shell=True).wait()
        
        return None
