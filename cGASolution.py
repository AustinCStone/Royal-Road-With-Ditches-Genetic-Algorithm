###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## All rights reserved       ##
###############################

from cSolution import *

### GA Solution
### Contains a solution for an N bit Genetic Algorithm


class cGASolution(cSolution):

    ### Function - cSolution::__init__
    ### Purpose  - Instasiate a solution object from the context file--ie the seed solution
    ### Input    - Context objet
    ### Output   - a seed solution
    def __init__ (self, ctx, N=None, parent=None):
        self._genome = 0L
        self._fitnessVal = float('-inf')
        self._ID = ctx.getID()
        self._N = N
        
        if(len != None):
            #create a string of
            self._genome = long(ctx.random.getrandbits(N))

    ### Function - cSolution::__str__
    ### Purpose  - return an "informal" string representation
    ### Input    - none
    ### Output   - string containing ID and fitness
    def __str__ (self):
        return bin(self._genome)

    def getGenome(self):
        return self._genome

    def setGenome(self, g):
        self._genome = g

    ##@todo: back port these to the base class and revise the population class accordingly
    def getRandomOrg(self,ctx):
        return cGASolution(ctx, self._N)

    def getChildOrg(self,ctx):
        child = cGASolution(ctx, self._N, self)
        child.setGenome(self._genome)
        child.setFitness(self._fitnessVal)

        return child
    
    

