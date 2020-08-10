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
        self.population = []
        self.newborn = []
        print("Generation created.")

    #This method prints the generation number when called.
    def __str__(self):
        return f"Generation: {self.gen}"

    #This method populates the generation.
    #Only for gen 0.
    def populate(self, history):
        for indiv in range(self.num):
            self.population.append(Individual(random.choice(self.p_1), random.choice(self.p_2), random.choice(self.p_3), random.choice(self.p_4)))
        #Calculates the merit for each individual.
        #Appends to history so we can keep track of parameters used.
        for i in range(len(self.population)):
            self.population[i].merit_calc()
            history.append(copy.deepcopy(self.population[i]))
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
        #Checks if there is a merit value already.
        #Calculates merit for new individuals.
        for i in range(len(self.population)):
            if self.population[i].merit == None:
                self.population[i].merit_calc()

    #Performs mating stage using genetic alogirthm.
    #Takes top 50% and randomly switches their parameters.
    def mating_stage(self, history):
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
        
        #Creates new individual.
        #Checks if it has been used already.
        #If it is a repeat, it takes the merit from the repeat so it is not recalculated.
        #Saves computational space and time.
        for i in range(len(top50)):
            add_to_history = True
            for j in range(len(parameter_mixing_list)):
                random.shuffle(parameter_mixing_list[j])
            new_individual = Individual(parameter_mixing_list[0].pop(), 
                                        parameter_mixing_list[1].pop(),
                                        parameter_mixing_list[2].pop(),
                                        parameter_mixing_list[3].pop())
            for j in range(len(history)):
                if new_individual.parameter_list == history[j].parameter_list:
                    new_individual = copy.deepcopy(history[j])
                    add_to_history = False
                    break
            if add_to_history == True:
                history.append(copy.deepcopy(new_individual))
            self.newborn.append(copy.deepcopy(new_individual))
