#import numpy as np
#import math
#import copy
#import matplotlib.pyplot as plt
#import random

class Individual:
    """
    A class which defines the parameters for each individual.
    The parameters are in a tuple and chosen randomly from a predetermined range.
    The merit is the sum of the individual parameters in this case.
    """

    def __init__(self, *ParameterList):
        self.parameter_list = list(ParameterList)
        self.merit = sum(self.parameter_list)
        #print("Individual created.")

    #This method prints the parameters and the merit of each individual when called.
    def __str__(self):
        for i in range(len(self.parameter_list)):
            print(f"p_{i+1}: {self.parameter_list[i]}")
        print(f"Merit: {self.merit}")
        return f""

    #This method calculates the merit after the parameters have been changed.
    def merit_calc(self):
        self.merit = sum(self.parameter_list)
        #print(self.merit)