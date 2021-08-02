import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def output_saved_data(data_in):
    """
    Prints the generation number, and each individual within that
    generation, with their parameters and merit value.

    Parameters:
        data_in = Passes in the data from the file so that the
                  data can be printed.
    """
    # Loops through each generation.
    for i in range(len(data_in)):
        print(f"Generation {data_in[i][0]}:")
        # Loops through each individual.
        # Excludes the first entry as it is the generation number,
        # not an individual.
        for j in range(len(data_in[0])):
            if j == 0:
                continue
            else:
                print(f"Sim {j}:")
                print(f"{data_in[i][j]}")


def axis_setter(data_in):
    """
    Collects the x and y axis from the data and puts them in
    their own lists, then returns them.

    Parameters:
        data_in = Passes in the data so that the x and y
                  axis can be populated.

    Variables:
        x_axis = Stores the values for the x-axis.

        y_axis = Stores the values for the y_axis.
    """
    x_axis = []
    y_axis = []

    # Loop through each generation.
    for i in range(len(data_in)):
        # Loop through each individual.
        for j in range(len(data_in[0])):
            # The 0 index is the generation number, so can be skipped.
            if j == 0:
                continue
            else:
                x_axis.append(data_in[i][0])
                y_axis.append(data_in[i][j].merit)
    return x_axis, y_axis


def data_plotter(x_axis, y_axis, gen_smoothing):
    """
    Plots the data onto a new figure and saves it.
    To work out the progress of the algorithm, the average merit for
    each generation is calculated and a curve is plotted.

    Parameters:
        x_axis = Passes the x-axis which is converted into a numpy
                 array.

        y_axis = Passes in the y-axis.

        gen_smoothing = Passes in the generation smoothing list.

    Variables:
        x_axis_ = Stores the x-axis as a numpy array.

        x_average = Stores the x-axis that is used for the progression
                    curve.

        y_average = Stores the average merit per generation.

        f = Stores the function that is used to plot the progression
            curve.

        x_fit = Stores the x-coordinates for the progression curve.

        y_fit = Stores the y-coordinates for the progression curve.
    """
    x_axis_ = np.array(x_axis)
    x_avg = np.array(gen_smoothing)
    y_avg = []

    for i in range(len(gen_smoothing)):
        y_avg.append(sum(merit_smoothing[i]) / len(merit_smoothing[i]))
    plt.xticks(list(range(0, len(x_axis), 3)))
    plt.plot(x_axis_, y_axis, 'o')

    if len(x_avg) == 1:
        pass
    else:
        f = interpolate.interp1d(x_avg, y_avg)
        x_fit = np.linspace(0, x_avg[-1], int((x_avg[-1] + 1) / 2))
        y_fit = f(x_fit)
        plt.plot(x_fit, y_fit, '-')

    plt.xlabel("Generation Number")
    plt.ylabel("Merit")
    plt.title("Progression of the Merit as Generation Number Increases.")
    plt.savefig("MeritProgressionAnalysis.png")
    plt.show()


if __name__ == "__main__":
    # Loads the data in as a list.
    data_in = np.load("GAData.npy", allow_pickle=True)
    curve_data_in = np.load("SmoothingData.npy", allow_pickle=True)
    gen_smoothing = curve_data_in[0]
    merit_smoothing = curve_data_in[1]

    output_saved_data(data_in=data_in)
    x_axis, y_axis = axis_setter(data_in=data_in)
    data_plotter(x_axis=x_axis,
                 y_axis=y_axis,
                 gen_smoothing=gen_smoothing)
