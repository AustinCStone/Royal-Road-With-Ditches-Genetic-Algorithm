###############################
## Python Evolution - v 0.1  ##
## A. W. Covert III, Ph. D   ##
## Austin Stone              ##
## All rights reserved       ##
###############################
class PE_SimulationOutput(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "PE_SimultaionOutputException: " + str(value)

class PE_PopulationParameters(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "PE_PopulationParametersException: incompatiable parameters were passed to the population" + str(value)
