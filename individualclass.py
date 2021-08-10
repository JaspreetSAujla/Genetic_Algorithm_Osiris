import h5py
import numpy as np
from os import listdir
import re


class Individual:
    """
    A class that defines an 'Individual' object.
    The input parameters are the parameters that are being investigated
    in the genetic algorithm.
    This class has the ability to change the input file(s) for the
    simulation, run the simulation, extract the merit value, and restore
    the input files to their original state, so that they can be used
    for the next generation.

    Note: ====== !!! This needs to be changed !!! ======
          The current merit is just the sum of the items in the
          ParameterList tuple. This was used as dummy data to test
          if the genetic algorithm was working.
          See merit_calc function for more details.

    Attributes:
        *ParameterList = When an instance of this class is
                         initialised, it can take any number of
                         arguments, which are all then stored into a
                         tuple.
                         Later converted into a list for convenience.

    Methods:
        __init__ = Initialises an instance of the 'Individual'
                   object and assigns the variables.

        __str__ = Returns the parameters along with their corresponding
                  values. Also returns the merit value.

        merit_calc = Calls the methods to change the input file(s), run
                     the simulation, extract the merit, and restore the
                     changes made to the input file(s).
                     Currently the merit is the sum of the parameters,
                     and needs to be changed.
                     Check merit_calc method for more details.

        change_file = This method changes the text in the input file(s)
                      to the desired input parameters.

        run_simulation = This method should run the simulation.
                         The code needs to be implemented still.

        list_files = Puts the data files into a tuple.

        extract_merit = Extracts the merit value from the input file.

        reverse_change = Restores the input file(s) to the original state
                         so that they can be used for the next
                         generation.
    """

    def __init__(self, *ParameterList):
        """
        Initialises an instance of the 'Individual' class.
        The class can take any number of arguments, and they are placed
        into a tuple called ParameterList. This is then turned into a
        list.

        Variables:
            self.parameter_list = Takes the argument that is passed
                                  from the method and converts the tuple
                                  into a list.

            self.merit = Stores the merit value. Set to None as there is
                         no merit calculated when the class in initialised.
        """
        self.parameter_list = list(ParameterList)
        self.merit = None

    def __str__(self):
        """
        Method returns the values of the parameters and the merit value.
        """
        # For loop used to cycle through all the parameters.
        dataList = [
            f"Parameter {i+1}: {self.parameter_list[i]}" for i in range(len(self.parameter_list))]

        return str(dataList)

    def merit_calc(self, input_file):
        """
        Method calculates the merit value used by changing the
        input file(s) with the desired parameters, running the
        simulation, extracting the merit value from the data, and
        restoring the input file(s) so that they can be used for the
        next generation.

        The run_simulation and extract_merit methods are commented
        out as the run_simulation method still needs to be written.
        The extract_merit method can only be used once the run_simulation
        method has been implemented.
        The self.merit variable is currently set by summing all the
        parameters together, as this was used as dummy data to test how
        well the algorithm functioned.

        Parameters:
            input_file = Passes in the input file that is used
                         to run the simulation.
        """
        # self.change_file(input_file)
        # The 2 methods below can be uncommented once the implementation
        # for the run_simulation method is complete.
        self.run_simulation()
        # self.extract_merit()
        # self.reverse_change(input_file)
        # The self.merit on the line below can be deleted once you
        # have the extract_merit and run_simulation method working.
        self.merit = sum(self.parameter_list)

    def run_simulation(self):
        """
        This method will run the simulation, which will return
        some data files that can be used to extract the merit
        value.
        """
        pass

    def list_files(self, directory):
        """
        This method takes the data files that are returned from the
        simulation and places them into a tuple.

        Parameters:
            directory = ...

        Variables:
            s0 = ...

            e0 = ...
        """
        s0 = 'RAW-Beam'
        e0 = '.h5'
        return (f for f in listdir(directory) if (s0 in f and e0 in f))

    def extract_merit(self):
        """
        This method goes through the data files and extracts the
        merit value.

        Note: Elisabetta gave me this method, so I am not exactly
              sure how it works.
        """
        dirname = 'MS/RAW/Beam'
        files = self.list_files(dirname)
        it_old = 0

        for f in files:
            fullfilename = dirname + '/' + f
            print(fullfilename)
            try:
                it_new = int(
                    re.search(
                        'RAW-Beam-(.+?).h5',
                        fullfilename).group(1))
                if it_new > it_old:
                    it_old = it_new
                    myfile = fullfilename
            except BaseException:
                pass

        hf = h5py.File(myfile, 'r')
        #q = hf.get('q').value
        #ene = hf.get('ene').value
        q = np.abs(hf['q'][:])
        ene = hf['ene'][:]

        qene = q * ene
        tot_qene = sum(qene)
        tot_charge = sum(q)
        ave = tot_qene / tot_charge

        standard_deviation = np.sqrt(sum(q * (ene - ave)**2 / tot_charge))
        self.merit = standard_deviation / ave