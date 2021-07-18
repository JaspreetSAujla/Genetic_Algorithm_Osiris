from generationclass import Generation
import copy
import matplotlib.pyplot as plt
import numpy as np
#from numpy.polynomial.polynomial import polyfit
#from scipy.interpolate import make_interp_spline, BSpline
from scipy import interpolate

#Saves the data into lists to be plotted and saved.
def data_saver(gen_in_list, gen_x_axis, merit_y_axis, data, merit_smoothing, gen_smoothing):
    item_in_data = []
    item_in_data.append(gen_in_list.generation)
    gen_smoothing.append(gen_in_list.generation)
    for i in range(len(gen_in_list.population)):
        gen_x_axis.append(gen_in_list.generation)
        item_in_data.append(gen_in_list.population[i])
        merit_y_axis.append(gen_in_list.population[i].merit)
        merit_smoothing[gen_in_list.generation].append(gen_in_list.population[i].merit)
    data.append(copy.deepcopy(item_in_data))


#Plots the data.
#To plot a line of best fit, x axis has to be numpy array.
#Works out average merit for each generation.
#Plots a curve from that.
#Deletes the previous figure and replaces it with the current one.
def data_plotter(gen_x_axis, merit_y_axis, gen_smoothing, merit_smoothing):
    try:
        plt.clf()
    except:
        pass
    x_axis = np.array(gen_x_axis)              #This avoids type error.
    x_avg = np.array(gen_smoothing)
    y_avg = []
    for i in range(len(gen_smoothing)):
        y_avg.append(sum(merit_smoothing[i])/len(merit_smoothing[i]))
    label_x_axis = list(range(0, len(x_axis), 3))
    plt.xticks(label_x_axis)
    plt.plot(x_axis, merit_y_axis, 'o')
    if len(x_avg) == 1:
        pass
    else:
        f = interpolate.interp1d(x_avg, y_avg)
        x_fit = np.linspace(0, x_avg[-1], int((x_avg[-1] + 1)/2))
        y_fit = f(x_fit)
        plt.plot(x_fit, y_fit, '-')
    plt.xlabel("Generation Number")
    plt.ylabel("Merit")
    plt.title("Progression of the Merit as Generation Number Increases.")
    plt.savefig("MeritProgression.png")