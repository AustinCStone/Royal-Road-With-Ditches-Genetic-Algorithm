###############################
## MyPDBPareser     - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################

from re import split
from os import exists

#store and parse data out of a PDB file--currently only stores the raw dump and a list of residues
class cMyPDBParse(object):

    ### Function - cMyPDBParse::__init__
    ### Purpose  - Instasiate a solution object from the context file--ie the seed solution
    ### Input    - Filename of pdb file
    ### Output   - a cMyPDBParer Object
    def __init__ (self, fileName):
        if(exists(filename)):

            #dictionary of residual values for translation purposes
            self.resdict = { 'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F', \
                             'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L', \
                             'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', \
                             'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y' }
            

            #nab the file
            fp = open(filename,'r')
            self.fileDump = fp.readlines()
            fp.close()

            #get the file length
            size = len(self.fileDump)

            #split the atom vecotrs
            for i in range(0,size):
                if(self.fileDump[i][0:3] == "ATOM"):
                    self.fileDump[i] =  split('\s+',self.fileDump)
                else:   #end of usefull stuff
                    break

            self.residue = self.parseResidue()

    ### Function - cMyPDBParse::parseResidue
    ### Purpose  - 
    ### Input    - 
    ### Output   - 
    def parseResidue(self):

        #grab the last residue position
        lastPos = self.fileDump[-1][5]

        
        
        
