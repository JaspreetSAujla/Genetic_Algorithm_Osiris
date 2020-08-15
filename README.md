# Genetic_Algorithm_Osiris
Genetic Algorithm used to minimise the energy spread of electrons for an electron beam injected LWFA

# main.py:
    Contains the main function and the initial variables which need to be used.
    Loops over each generation until the max generation limit has been reached.
    Saves the data into a file once the simulation has finished.
    This is the file to run!!!
    THINGS TO CHANGE:
        If you want to change the number of generations, then change the max_gen variable to what you desire.

# generationclass.py:
    Defines each generation.
    Populates the very first generation randomly from the initial parameters.
    Performs the mating stage for the individuals.
    Repopulates the for the next generation.
    Also outputs the individuals with their figure of merit.
    THINGS TO CHANGE:
        If you want to change the number of individuals, then change the num= variable in the argument of the __init__ method. Also this needs to be an even number!!!
        If you want to change the values/range of values in a paramter, simply change the self.p_(1..4) variables with your desired range.
        If you want to add/remove the number of parameters there are to optimise, then you need to create/remove another self.p_() variable. As well as this, you need to add/remove this variable in the populate, crossover_stage and mutation_stage methods, inside the Individual argument, so that each individual recieves the new paramter.
        NOTE: In the crossover_stage and mutation_stage, the Individual argument has self.parameter_mixing_list with the appropriate index for the variable, make sure to put the appropriate index.

# individualclass.py:
    Defines each individual.
    Works out the figure of merit when function is called.
    WHAT TO CHANGE:
        If you change the number of parameters that are being optimised, then you will need to update the change_file and reverse_change methods to reflect where the parameters are in the input file.

# PlottingFile.py:
    Saves the data into lists.
    Two set of lists used for plotting.
    Another list used for saving the data to a file.
    A method which plots the data and saves the plot as a png.
    Plots figure of merit against generation with a line of best fit.

# DataAnalysis.py:
    This script is to be used at a later date after the simulation has done.
    Imports the data files and prints the generations, individuals and figure of merit.
    Then plots the figure of merit against generation number and saves and shows the plot.

# inputfile(1..10).inp:
    These files contain the simulation parameters. The parameters that are being optimised will automatically update.
    THINGS TO CHANGE:
        If you need to change a parameter that is not being optimised (e.g. the number of cores being used), then you need to change this manually in all the files.
        If you change the number of individuals, then you will have to change the number of input files that are present. One input file per individual. The input files get recycled for the next generation and update automatically.
