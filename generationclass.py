#import numpy as np
#import math
import copy
import matplotlib.pyplot as plt
import random
from individualclass import Individual

class Generation:
    """
    A class which defines the generation from the given individuals.
    The init method also has the constraints for the parameters.
    Once the individuals are created, they are put into a population list.
    """

    def __init__(self, gen=0, num=10, mutation=0):
        self.gen = gen                  # Generation number
        self.num = num                  # Number of individuals per generation
        self.mutation = mutation        # Rate of mutation
        self.p_1 = list(range(0, 6))
        self.p_2 = list(range(0, 6))
        self.p_3 = list(range(0, 6))
        self.p_4 = list(range(0, 6))
        self.ran_num_list = list(range(-2, 4))
        self.population = []
        print("Generation created.")

    #This method prints the generation number when called.
    def __str__(self):
        return f"Generation: {self.gen}"

    #This method populates the generation.
    #Only for gen 0.
    def populate(self):
        for indiv in range(self.num):
            self.population.append(Individual(random.choice(self.p_1), random.choice(self.p_2), random.choice(self.p_3), random.choice(self.p_4)))
        print("Generation populated.")

    #Prints the current progress of the algorithm.
    def output_current_status(self):
        print(self)
        for i in range(len(self.population)):
            print(f"Sim {i+1}:")
            print(f"{self.population[i]}")

    #Increases Generation number for the class.
    #Works out the new variables.
    def mating_stage(self):
        self.gen += 1
        #Loops through individuals.
        for i in range(len(self.population)):
            #Loops through each parameter and changes it.
            for j in range(len(self.population[0].parameter_list)):
                self.population[i].parameter_list[j] += random.choice(self.ran_num_list)
            self.population[i].merit_calc()

    #This creates a new population based on the previous one.
    #Will be used for gen1 and above.
    def repopulate(self, PreviousPop):
        self.population = PreviousPop
