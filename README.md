# Genetic_Algorithm_Osiris
Genetic Algorithm used to minimise the energy spread of electrons for an electron beam injected LWFA

# main.py:
    Contains the main function and the initial variables which need to be used.
    Loops over each generation until the max generation limit has been reached.
    Saves the data into a file once the simulation has finished.
    This is the file to run!!!

# generationclass.py:
    Defines each generation.
    Populates the very first generation randomly from the initial parameters.
    Performs the mating stage for the individuals.
    Repopulates the for the next generation.
    Also outputs the individuals with their figure of merit.

# individualclass.py:
    Defines each individual.
    Works out the figure of merit when function is called.

# PlottingFile.py:
    Saves the data into lists.
    One set of lists used for plotting.
    Another list used for saving the data to a file.
    A method which plots the data and saves the plot as a png.
    Plots figure of merit against generation with a line of best fit.

# DataAnalysis.py:
    This script is to be used at a later date after the simulation has done.
    Imports the data file and prints the generations, individuals and figure of merit.
    Then plots the figure of merit against generation number and saves and shows the plot.
