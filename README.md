# Genetic_Algorithm_Osiris
Genetic Algorithm used to minimise the energy spread of electrons for an 
electron beam injected LWFA.

# How To Run The Algorithm:
Open the 'main.py' file and run it.

# How To Change The Values Used In The Algorithm:
Open the 'ga_inputs.json' file. There will be a list of variables that 
can be changed. 
    "max_generation_number" = Is the maximum number of generations that 
                              algorithm will go through.
    "num_of_individuals" = Is the number of individuals created per 
                           generation.
                           THIS NEEDS TO BE AN EVEN NUMBER!!!
    "plasma_density" = Is one of the parameters being investigated.
                       This is a discrete list of normalised plasma 
                       densities.
    "laser_spot_size" = Is one of the parameters being investigated.
                        This is a discrete list of normalised values 
                        for the laser spot size.
    "jitter_distance_range" = Is a list that stores the minimum range, 
                              maximum range, and the step size of the 
                              jitter distance.
    "laser_focus_range" = Is a list that stores the minimum range, 
                          maximum range, and step size of the laser 
                          focus.

## Adding(Removing) A Parameter:
To add(remove) a parameter, add it to the json file.
Open 'generationclass.py and add(remove) the parameter from the class 
variables. 
Go into the 'populate' method, and add(remove) the parameter from the 
initialisation of the 'Individual' object.
Go into 'crossover_stage' method, and add(remove) the parameter from 
the initialisation of the 'Individual' object.
Go into 'mutation_stage' method and add(remove) the parameter from the 
initialisation of the 'Individual' object.
Then add(remove) an elif block with the appropriate arguments for the 
'Individual' object.
Open 'individualclass.py' and add(remove) the parameter from the 
'change_file' and 'reverse_change' methods, so that they mirror what 
is in the input file.

# main.py:
This is the file that needs to be run to start the genetic algorithm.

# gaclass.py:
Class that defines a genetic algorithm object. This class is used 
to define the initial variables of the algorithm and run it.

# generationclass.py:
This class contains the code which performs the bulk of the genetic 
algorithm. For each generation, the class will populate the generation 
with a given number of individuals, where the parameters are chosen 
randomly, calculate the merit value for each individual, take the top 
50% of individuals, and repopulate the next generation. 
There are also methods which introduce mutations, which avoid the 
algorithm getting stuck in a local maximum/minumum, by introducing 
random parameters.

# individualclass.py:
A class that defines an 'Individual' object.
The input parameters are the parameters that are being investigated 
in the genetic algorithm.
This class has the ability to change the input file(s) for the 
simulation, run the simulation, extract the merit value, and restore 
the input files to their original state, so that they can be used 
for the next generation.

# DataAnalysis.py:
This script is to be used at a later date after the simulation has done.
Imports the data files and prints the generations, individuals and figure 
of merit. Then plots the figure of merit against generation number and 
saves and shows the plot.

# inputfile(1..10).inp:
These files contain the simulation parameters. The parameters that are 
being optimised will automatically update.

## Things To Change:
If you need to change a parameter that is not being optimised 
(e.g. the number of cores being used), then you need to change this 
manually in all the files.
If you change the number of individuals, then you will have to change 
the number of input files that are present (for this current 
implementation). 
One input file per individual. The input files get recycled for the 
next generation and update automatically.