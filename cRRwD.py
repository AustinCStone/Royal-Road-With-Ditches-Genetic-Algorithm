###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################

### Interface between cSolution and the actual simulation
### Base class

from cSimulationInterface import *

class cRRwD(cSimulationInterface):

    def __init__ (self, ctx, N, K, w,u, penelty):
        self._N = N
        self._K = K
        self._w = w
        self._p = penelty
        self._u = u

        self._solutionLen = self._N * self._K

        #block templates
        self._A = (2**(K) - 1)
        self._B = ((self._A >> w) << w) & self._A
        self._C = (self._A>>u) & self._A
        
        return None

    def getSolutionLen():
        return self._solutionLen

    ### Function - cSimulationInterface::evalutateOrgFitness
    ### Purpose  - run the solution through the simulation to get fitness
    ### Input    - None
    ### Output   - Boolean indicating success or failure of the simulation
    def evaluateOrgFitness(self,ctx,org):

        genome = org.getGenome()

        fitness = self._evalFitness(genome)
        
        org.setFitness(fitness)
        
        return fitness

    ### Function - cSimulationInterface::mutateAndEvalutateOrgFitness
    ### Purpose  - run the solution through the simulation to mutate it, set the solutions fitness
    ### Input    - None
    ### Output   - Boolean indicating success or failure of the simulation
    def mutateAndEvaluateOrgFitness(self,ctx,org):
        genome = org.getGenome()

        genome ^= 2**(ctx.random.randint(0,self._solutionLen-1))

        fitness = self._evalFitness(genome)
        
        org.setFitness(fitness)
        org.setGenome(genome)
        
        return fitness
#print evalFitness(self, 11001111000000000000)
#eval fitness modified to simulate negative epistasis of beneficial mutations
#additional variable bCounter is added to keep track of the number of b blocks
#the number of b blocks determines the extent of the negative epistatis
#it is currently set to add to the exponent 1/bCounter
    def _evalFitness(self, genome):
       # exponent = 1.0
        epiConst = 2
        coef = 1.0
        D_block = False
        E_block = False 
        bCounter = 0.0
        cCounter = 0.0 
        previousAddC = 0.0
        previousAddB = 0.0
        if ((self._getPos(genome, 1) == self._B) or (self._getPos(genome, 1) == self._C)):
            if self._getPos(genome, 1) == self._B:
                bCounter = 2.0
                previousAddB = 2.0
            if self._getPos(genome, 1) == self._C:
                cCounter = 2.0
                previousAddC = 2.0
            for i in range(2, self._N):
                block = self._getPos(genome, i)
                if(block == self._B and D_block == False and E_block == False):
                    # print "B" + bin(block)
                    bCounter += previousAddB*epiConst
                    previousAddB = previousAddB*epiConst
                    #exponent += (1.0/(bCounter**(bCounter/(self._N/3.5))))
                elif (block == self._C and D_block == False and E_block == False):
                    if cCounter == 0.0:
                        cCounter = 2.0
                        previousAddC = 2.0
                    else:
                        cCounter += previousAddC*epiConst
                        previousAddC = epiConst*previousAddC
                    #exponent += (1.0/(cCounter**(cCounter/(self._N/3.5)))) 
                elif (block == self._A):
                    return coef*(cCounter+bCounter)
                elif ((block>>self._w)<<self._w)==self._B:
                    #print "X" + bin(block)
                    D_block == True
                    coef = 1.0 - self._p
                elif (((block<<self._u)& self._A)>>self._u)==self._C:
                    #print "X" + bin(block)
                    E_block == True
                else:
                    return 0.0
        else:
            return 0.0

        return 0.0
#this is part of the problem, it shifts it over N.. Should shift over by the
#genome length incase some genomes aren't maximum length maybe?    
    def _getPos(self, genome, i):
        return (genome >> ((self._N - i) * self._K)) & self._A
