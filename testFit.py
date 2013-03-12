#driver program to determine errors 



from sys import argv
from os import mkdir
from os.path import exists

from cContext import *
from cGASolution import *
from cRRwD import *
from cGAPopulation import *

## Main driver program

## Read in input file

#verify the inputs

    
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
#changed the fitness penalty to zero
sim = cRRwD(ctx, N,K,w,0.0)
print bin(seed.getGenome())
print sim._evalFitness(seed.getGenome())
