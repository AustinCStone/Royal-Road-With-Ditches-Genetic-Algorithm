###############################
## Protien Evolution - v 0.1 ##
## A. W. Covert III, Ph. D   ##
## All rights reserved       ##
###############################

from sys import argv

from cContext import *
from cSolution import *
from cPopulation import *
from cRosettaBackRubSim import *
from cPE_Exceptions import *


## Main driver program

## Read in input file

#verify the inputs
if(len(argv) != 3):
    print "Error, takes exactly 3 arguments <script> <random seed> <options file>, " + str(len(argv)) + " arguments detected."
    quit()


## Create context object -- reads in option file and returns 
ctx = cContext(argv[1], argv[2])

## Create Seed individual
seed = cSolution(ctx)

## Instantiate a simulator interface to use
simulator = cRosettaBackRubSim()

## Set the simutlation executables
simulator.setFixBBExecutable("fixbb.linuxgccrelease")
simulator.setBackRubExecutable('backrub.linuxgccrelease')
simulator.setDockingExecutable('docking_protocol.linuxgccrelease')

## Create Population Object

population = cPopulation(ctx,simulator,seedOrg = seed)

quit()

print time.clock()

print population
print "--------------------------\n"

for x in range(0,500):
    print "Processed generation: " + str(population.step())
    print population
    print "--------------------------\n"


fp = open("test_1.dat","w")

fp.write(population.dumpSummaryStats())


## print "Initial  fit: " + str(seed.getFitness())
## print "Initial file: " + str(seed.getFilename())

## for x in range(0,100):
##     nOrg = cSolution(ctx, cOrg)
##     simulator.mutateAndEvaluateOrgFitness(nOrg)

##     print "New  fit: " + str(nOrg.getFitness())
##     print "New file: " + str(nOrg.getFilename())

##     if(nOrg.getFitness() == -float('inf')):
##         print "Lethal mutation... bailing out."
##         quit()

##     cOrg = nOrg
    
    

## Run experiment


