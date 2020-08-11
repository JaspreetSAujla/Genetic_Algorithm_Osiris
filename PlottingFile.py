from generationclass import Generation
import copy
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit

#Saves the data into lists to be plotted and saved.
def data_saver(gen_in_list, gen_x_axis, merit_y_axis, data):
    item_in_data = []
    item_in_data.append(gen_in_list.gen)
    for i in range(len(gen_in_list.population)):
        gen_x_axis.append(gen_in_list.gen)
        item_in_data.append(gen_in_list.population[i])
        merit_y_axis.append(gen_in_list.population[i].merit)
    data.append(copy.deepcopy(item_in_data))

#Plots the data.
#To plot a line of best fit, x axis has to be numpy array.
#Calculates polynomial of degree 1 from data and plots.
#Deletes the previous figure and replaces it with the current one.
def data_plotter(gen_x_axis, merit_y_axis):
    try:
        plt.clf()
    except:
        pass
    x_axis = np.array(gen_x_axis)              #This avoids type error.
    b, m = polyfit(x_axis, merit_y_axis, 1)
    label_x_axis = list(range(0, len(x_axis), 3))
    plt.xticks(label_x_axis)
    plt.plot(x_axis, merit_y_axis, 'o')
    plt.plot(x_axis, b + (m*x_axis), '-')
    plt.xlabel("Generation Number")
    plt.ylabel("Merit")
    plt.title("Progression of the Merit as Generation Number Increases.")
    plt.savefig("MeritProgression.png")
