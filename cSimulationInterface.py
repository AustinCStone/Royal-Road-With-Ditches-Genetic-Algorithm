###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################

### Interface between cSolution and the actual simulation
### Base class

class cSimulationInterface(object):

    def __init__ (self):

        return None

    ### Function - cSimulationInterface::evalutateOrgFitness
    ### Purpose  - run the solution through the simulation to get fitness
    ### Input    - None
    ### Output   - Boolean indicating success or failure of the simulation
    def evaluateOrgFitness(self,ctx,org):
        return True

    ### Function - cSimulationInterface::mutateAndEvalutateOrgFitness
    ### Purpose  - run the solution through the simulation to mutate it, set the solutions fitness
    ### Input    - None
    ### Output   - Boolean indicating success or failure of the simulation
    def mutateAndEvaluateOrgFitness(self,ctx,org):
        return True


        
