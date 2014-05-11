from sys import argv

from cContext import *
from cGASolution import *
from cRRwD import *

def newOrg(ctx, sim, parent):
    child = parent.getChildOrg(ctx)
    if(ctx.random.random() < ctx.mutRate):
        sim.mutateAndEvaluateOrgFitness(ctx,child)
    return child
        

def tournamentSelection(ctx, sim, population):
    pop = []

    maxFitness = 0.0
    maxGenome = 0.0
    
    for i in range(0, ctx.popSize):

        child = None
        
        org1 = population[ctx.random.randint(0,ctx.popSize-1)]
        org2 = population[ctx.random.randint(0,ctx.popSize-1)]
        
        if(org1.getFitness() >= org2.getFitness()):
            child = newOrg(ctx, sim, org1)
        else:
            child = newOrg(ctx, sim, org2)

        pop.append(child)

        if(child.getFitness() > maxFitness):
            maxFitness = child.getFitness()
            maxGenome = child.getGenome()

    return (pop, maxFitness, maxGenome)
            
    
    

## Main driver program

## Read in input file

#verify the inputs
if(len(argv) != 3):
    print "Error, takes exactly 3 arguments <script> <random seed> <options file>, " + str(len(argv)) + " arguments detected."
    quit()

## Create context object -- reads in option file and returns 
ctx = cContext(argv[1], argv[2])

#number of blocks
N = ctx.getInt("N")

#length of blocks
K = ctx.getInt("K")

#width of barrier
w = ctx.getInt("w")

## Create Seed individual
seed = cGASolution(ctx,N*K)

## intilize the seed organism to BAXX
seed.setGenome(long(ctx.get("seedSolution"),2))

## Create a simulation environment
sim = cRRwD(ctx, N,K,w,0.5)

## create a population with a list
population = []

##seed a population from the 
for i in range(0, ctx.popSize):
    population.append(newOrg(ctx, sim, seed))

print "Initial fitness: %s" % str(sim.evaluateOrgFitness(ctx, seed))

for i in range(1,ctx.numGen):
    population, maxFit, maxGenome = tournamentSelection(ctx, sim, population)
    print "Processing Geneeration %s, max fit: %s, max genome: %s" % (str(i), str(maxFit), bin(maxGenome))

