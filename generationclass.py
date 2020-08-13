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

    def __init__(self, gen=0, num=10, mutation=2):
        self.gen = gen                  # Generation number
        self.num = num                  # Number of individuals per generation
        self.mutation = mutation        # Rate of mutation
        self.p_1 = list(range(0, 26))
        self.p_2 = list(range(0, 26))
        self.p_3 = list(range(0, 26))
        self.p_4 = list(range(0, 26))
        #self.p_test = [0, 1, 3, 6, 7, 9, 11, 12]
        self.population = []
        self.parameter_mixing_list = []
        self.newborn = []
        print("Generation created.")


    #This method prints the generation number when called.
    def __str__(self):
        return f"Generation: {self.gen}"


    #This method populates the generation.
    #Only for gen 0.
    def populate(self, history):
        for indiv in range(self.num):
            self.population.append(Individual(random.choice(self.p_1),
                                              random.choice(self.p_2),
                                              random.choice(self.p_3),
                                              random.choice(self.p_4)))
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
    def repopulate(self, NewPop, history):
        self.population = NewPop
        #Checks if there is a merit value already.
        #Calculates merit for new individuals.
        for i in range(len(self.population)):
            if self.population[i].merit == None:
                self.population[i].merit_calc()
                history.append(copy.deepcopy(self.population[i]))


    #Performs mating stage using genetic alogirthm.
    #Takes top 50% and randomly switches their parameters.
    def mating_stage(self, history):
        top50 = []
        #List comprehension to make right sized list.
        self.parameter_mixing_list = [[] for i in range(len(self.population[0].parameter_list))]

        #Key takes a function.
        #operator.attrgetter = '.' as in self.merit.
        #Reverse makes it highest to lowest.
        self.population.sort(key=operator.attrgetter('merit'), reverse=False)
        for i in range(int(len(self.population)/ 2)):
            top50.append(self.population[i])
            self.newborn.append(self.population[i])
            for j in range(len(top50[0].parameter_list)):
                #Puts p_(1)'s in one sublist, p_(2)'s in another sublist etc.
                self.parameter_mixing_list[j].append(top50[i].parameter_list[j])
        for i in range(len(top50)):
            chance_of_mutation = random.choice(range(0, 11))
            if chance_of_mutation <= self.mutation:
                self.mutation_stage(history)
            else:
                self.crossover_stage(history)
        #Caps mutation rate at 60%
        if self.mutation == 6:
            pass
        else:
            self.mutation += 1


    #Creates new individual.
    #Checks if it has been used already.
    #If it is a repeat, it takes the merit from the repeat so it is not recalculated.
    #Saves computational space and time.   
    def crossover_stage(self, history):
        for j in range(len(self.parameter_mixing_list)):
            random.shuffle(self.parameter_mixing_list[j])
        new_individual = Individual(self.parameter_mixing_list[0].pop(), 
                                    self.parameter_mixing_list[1].pop(),
                                    self.parameter_mixing_list[2].pop(),
                                    self.parameter_mixing_list[3].pop())
        for j in range(len(history)):
            if new_individual.parameter_list == history[j].parameter_list:
                new_individual = copy.deepcopy(history[j])
                break
        self.newborn.append(copy.deepcopy(new_individual))


    #Performs the mutation.
    def mutation_stage(self, history):
        mutation_parameter = random.choice(range(len(self.parameter_mixing_list)))
        for j in range(len(self.parameter_mixing_list)):
            random.shuffle(self.parameter_mixing_list[j])
        if mutation_parameter == 0:
            new_individual = Individual(random.choice(self.p_1),
                                        self.parameter_mixing_list[1].pop(),
                                        self.parameter_mixing_list[2].pop(),
                                        self.parameter_mixing_list[3].pop())
        elif mutation_parameter == 1:
            new_individual = Individual(self.parameter_mixing_list[0].pop(),
                                        random.choice(self.p_2),
                                        self.parameter_mixing_list[2].pop(),
                                        self.parameter_mixing_list[3].pop())
        elif mutation_parameter == 2:
            new_individual = Individual(self.parameter_mixing_list[0].pop(),
                                        self.parameter_mixing_list[1].pop(),
                                        random.choice(self.p_3),
                                        self.parameter_mixing_list[3].pop())
        elif mutation_parameter == 3:
            new_individual = Individual(self.parameter_mixing_list[0].pop(),
                                        self.parameter_mixing_list[1].pop(),
                                        self.parameter_mixing_list[2].pop(),
                                        random.choice(self.p_4))
        for j in range(len(history)):
            if new_individual.parameter_list == history[j].parameter_list:
                new_individual = copy.deepcopy(history[j])
                break
        self.newborn.append(copy.deepcopy(new_individual))    