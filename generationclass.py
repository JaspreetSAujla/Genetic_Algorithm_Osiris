#import numpy as np
#import math
import copy
import matplotlib.pyplot as plt
import random
from individualclass import Individual
import operator

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
        self.newborn = []
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

    #This creates a new population based on the previous one.
    #Will be used for gen1 and above.
    def repopulate(self, NewPop):
        self.population = NewPop

    #Performs mating stage using genetic alogirthm.
    #Takes top 50% and randomly switches their parameters.
    def mating_stage(self):
        top50 = []
        #List comprehension to make right sized list.
        parameter_mixing_list = [[] for i in range(len(self.population[0].parameter_list))]

        #Key takes a function.
        #operator.attrgetter = '.' as in self.merit.
        #Reverse makes it highest to lowest.
        self.population.sort(key=operator.attrgetter('merit'), reverse=True)
        for i in range(int(len(self.population)/ 2)):
            top50.append(self.population[i])
            self.newborn.append(self.population[i])
            for j in range(len(top50[0].parameter_list)):
                #Puts p_(1)'s in one sublist, p_(2)'s in another sublist etc.
                parameter_mixing_list[j].append(top50[i].parameter_list[j])
            
        #Appends 50% new individuals with random attributes from top50.
        for i in range(len(top50)):
            self.newborn.append(Individual(random.choice(parameter_mixing_list[0]), 
                                           random.choice(parameter_mixing_list[1]),
                                           random.choice(parameter_mixing_list[2]),
                                           random.choice(parameter_mixing_list[3])))

