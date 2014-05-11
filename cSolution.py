###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################


from cPE_Exceptions import *

### Solution Class
### Wraper for solution classes -- contains an inidividual solution and all assoicated functionality

### @TODO: add a "sameAsParent" value to avoid duplicate simulations

class cSolution(object):


    ### Function - cSolution::__init__
    ### Purpose  - Instasiate a solution object from the context file--ie the seed solution
    ### Input    - Context objet
    ### Output   - a seed solution
    def __init__ (self, ctx, parent=None):
        self._fitnessVal = -inf

    ### Function - cSolution::__str__
    ### Purpose  - return an "informal" string representation
    ### Input    - none
    ### Output   - string containing ID and fitness
    def __str__ (self):
        return "solution"

    ### Function - cSolution::__cmp__
    ### Purpose  - Compare two orgs; return -1 if less than 0 if equal, 1 if more 
    ### Input    - org to compare
    ### Output   - Result of comparision
    def __cmp__(self, other):
        if self._fitnessVal < other._fitnessVal:
            return -1
        elif self._fitnessVal == other._fitnessVal:
            return 0
        else:
            return 1
        
            
    ### Function - cSolution::getFitness
    ### Purpose  - get the fitness value
    ### Input    - none
    ### Output   - Float representing fitness        
    def getFitness(self):
        return self._fitnessVal

    ### Function - cSolution::getFilename
    ### Purpose  - Get the filename of the associated solution file
    ###            Note that not all solution classes will contain this
    ### Input    - none
    ### Output   - filename        
    def getFilename(self):
        return self._fileName

    ### Function - cSolution::setFitness
    ### Purpose  - get the fitness value
    ### Input    - Float representing fitness
    ### Output   - none
    def setFitness(self, newFitness):
        self._fitnessVal = newFitness

    ### Function - cSolution::setFilename
    ### Purpose  - Set the filename of the associated PDB file and reset the residue and PDBFile information
    ### Input    - pdb filename
    ### Output   - none        
    def setFilename(self, newFilename):
        self._fileName = newFilename

        self._PDBFile = cMyPDBParser(self._fileName)

        self._residue = self._PDBFile.getResidue()

        self._resStr = self._createResString()

        
    ### Function - cSolution::getResidue
    ### Purpose  - accessor to return a dict containing the residue
    ### Input    - none
    ### Output   - list continaing tuples of residues and chain IDs
    def getResidue(self):
        return self._residue

    ### Function - cSolution::getResidueStr
    ### Purpose  - accessor to return a string containing the residue
    ### Input    - none
    ### Output   - string containing the residue 
    def getResidueStr(self):
        return self._resStr


    ### Function - cSolution::getID
    ### Purpose  - accessor to return the org ID
    ### Input    - none
    ### Output   - ID
    def getID(self):
        return self._ID

    ### Function - cSolution::getAAcodes
    ### Purpose  - accessor to return a list of aminoacid codes
    ### Input    - none
    ### Output   - a list continaing the relevant amino acid encodings
    def getAAcodes(self):
        return self._PDBFile.getAAcodes()


