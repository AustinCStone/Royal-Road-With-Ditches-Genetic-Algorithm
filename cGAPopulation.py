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
from numpy import *
from cSolution import *
from cPE_Exceptions import *
from cStats import *


### Population Class
### Polution base class -- Constructs and stores the popuation, handles the selection of each new generation

### This population class uses a simple rank based selection algorithm

class cGAPopulation(object):


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

        self.__maxID = -1
        self.__maxOrg = None

       
         

        #size of each partion for the rank based selection
        self.__partionSize = self.__ctx.popSize / self.__partions

        #either create a population form a seed organism or copy an exisiting population
        if(seedOrg is not None):
            self.__instansiatePopulationFromOrg(seedOrg)

        if(copyPopulation is not None):
            self.__deepCopyPopulation(copyPopulation)

        #print self.fits
        #when we are done creating it the population array should always be sorted
        #subsequent populations that are the result of selection should also be sorted
        self.__population.sort()
        #print self.__population

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
       # print self.fits
        #create a new population
        newPopulation = []

        #total fitness
        totalFit = 0.0
        
        #max fitness and ID
        maxFitness = float('-inf')
        maxID = None

        #count of births
        count = 0

        #mut count
        nMutations = 0

        #increment the generation count
        self.__ctx.currGen = self.__ctx.currGen + 1
        new_fits = zeros(self.__ctx.popSize)
        #fill the population with the appropriate number of orgs
        for x in range(0,self.__ctx.popSize):

            #return a copy of a lucky parent
            newOrg = self.__select(x,self.fits)

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

            totalFit = totalFit + newOrg._fitnessVal
            new_fits[x]=newOrg._fitnessVal
            if(newOrg._fitnessVal > maxFitness):
                maxFitness = newOrg._fitnessVal
                self.__maxID = newOrg.getID()
                self.__maxOrg = newOrg

            #append the new org to the population
            newPopulation.append(newOrg)

       
        self.__stats.addGenStats(averageFit = float(totalFit/count), maxFit = maxFitness, maxID = self.__maxID, nBirths = count, nMuts = nMutations)
        self.fits=cumsum((new_fits)/(totalFit))
       # print self.fits
        
        #make sure the new list is sorted
        #newPopulatio


        #finaly, assign the new population 
        self.__population = newPopulation

        #return the current generation number for shits and giggles
        return self.__ctx.currGen
    #returns cummulative fitness array 
    def __getcumfits(self):
        fits = zeros(self.__ctx.popSize-1,dtype="f")
        for i in range(self.__ctx.popSize-1):
            fits[i]=self.__population[i].getFitness()
        fits = cumsum(fits/sum(fits))
        return fits 

    def binary_search(self,seq, t):
        min = 0; 
        max = len(seq) - 1
        while 1:
            if max == min:
                mid = t-seq[min]
                if mid<=0: #this means the comparison item is to the left and less than the random number
                    if min==0:
                        return min
                    else:
                        comparison = seq[min-1]-t
                    if comparison<=mid:
                        return min
                    else:
                        return min-1 
                else: #this means the comparison item is to the right and is greater than the random number
                    if min+1==len(seq):
                        return min
                    else:
                        comparison = t-seq[min+1]
                    if mid<=comparison:
                        return min
                    else:
                        return min+1
            elif max<min:
                lower = t-seq[max]
                upper = t-seq[min]
                if upper <= lower:
                    return min
                else:
                    return max
            m = (min + max) / 2
            if seq[m] < t:
                min = m + 1
            elif seq[m] > t:
                max = m - 1
            else:
                return m
    ### Function - cPopulation::__select
    ### Purpose  - perform tornament selection on the population
    ### Input    - None
    ### Output   - index of selected organism
    def __select(self, round,fits):
        child = None
        
        
        search = self.__ctx.random.random()
        #index = self.binary_search(fits,search)
        index = searchsorted(fits,search,side='left')
       # if self.__ctx.currGen == 70 or self.__ctx.currGen == 69:
        #    print fits[index-1], fits[index]
         #   print search, index
          #  print self.__population[index].getFitness()
           # print self.__population[index-1].getFitness()
           # if index+1 < len(self.__population):
            #    print self.__population[index+1].getFitness()
        child = self.__population[int(index)].getChildOrg(self.__ctx)
        return child

    ### Function - cPopulation::__instansiatePopulationFromOrg
    ### Purpose  - instansiate a new population from a single seed organism
    ### Input    - seed organism
    ### Output   - None, assigns the new organisms to self.__population
    ### @TODO    - Refactor this into two versions with and without the job manager
    def __instansiatePopulationFromOrg(self,seed):

        #initialize the fitness of the seed organism
        self.__sim.evaluateOrgFitness(self.__ctx,seed)

        #this is the first generation, so we set the generation number to 1
        #we wait to do this here so that the seed org has generation 0
        self.__ctx.currGen = 1

        self.fits = zeros(self.__ctx.popSize)

        maxFit = -1
        maxID = -1

        #initialize and evalutate a popualtion of mutants
        for x in range(0,self.__size):

            #create a new org
            newOrg = seed.getChildOrg(self.__ctx)
            
            #check to see if we mutate
            if(self.__ctx.mutRate < self.__ctx.random.random()):
                #mutate
                self.__sim.mutateAndEvaluateOrgFitness(self.__ctx,newOrg)
                
            else:
                #no need to mutate
                #still need to evaluate to set the generation number
                self.__sim.evaluateOrgFitness(self.__ctx,newOrg)
                
            if(newOrg.getFitness() > maxFit):
                maxID = newOrg.getID()
                maxFit = newOrg.getFitness()
                self.__maxOrg = newOrg

            self.fits[x] = newOrg.getFitness()

            #tack on the new mutator
            self.__population.append(newOrg)

        self.fits=cumsum(self.fits/sum(self.fits))
        self.__maxID = maxID
       # print self.__maxID
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

    def getMaxOrg(self):
        return self.__maxOrg
       # newPopulation = self.__population
       # newPopulation.sort()
       # return newPopulation[-1]         
       #return self.__maxID
   
