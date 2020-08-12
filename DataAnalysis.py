import numpy as np
from generationclass import Generation
from individualclass import Individual
import math
import copy
import matplotlib.pyplot as plt
import random
#from numpy.polynomial.polynomial import polyfit
from scipy import interpolate

#4 y axis because 4 simulation objects.
x_axis = []
y_axis = []

#Loads the data in as a list.
data_in = np.load("GAData.npy", allow_pickle=True)

curve_data_in = np.load("SmoothingData.npy", allow_pickle=True)

gen_smoothing = curve_data_in[0]
merit_smoothing = curve_data_in[1]

#Prints the generation and the variables along with the merit value.
#Loop for the generation.
def output_saved_data():
    for i in range(len(data_in)):
        print(f"Generation {data_in[i][0]}:")
        #Loops through each individual.
        #Excludes the first entry as it is gen number, not an individual.
        for j in range(len(data_in[0])):
            if j == 0:
                continue
            else:
                print(f"Sim {j}:")
                print(f"{data_in[i][j]}")

#Collects the x and y axis from the data and puts it in a list.
def axis_setter():
    for i in range(len(data_in)):
        for j in range(len(data_in[0])):
            if j == 0:
                continue
            else:
                x_axis.append(data_in[i][0])
                y_axis.append(data_in[i][j].merit)

#Loops to create a plot.
#Creates a line of best fit from the data,
#X axis in a numpy array to avoid error.
def data_plotter():
    x_axis_ = np.array(x_axis)                            #avoids Type error.
    x_avg = np.array(gen_smoothing)
    y_avg = []
    for i in range(len(gen_smoothing)):
        y_avg.append(sum(merit_smoothing[i])/len(merit_smoothing[i]))
    label_x_axis = list(range(0, len(x_axis), 3))
    plt.xticks(label_x_axis)
    plt.plot(x_axis_, y_axis, 'o')
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
    plt.savefig("MeritProgressionAnalysis.png")
    plt.show()


if __name__ == "__main__":
    output_saved_data()
    axis_setter()
    data_plotter()