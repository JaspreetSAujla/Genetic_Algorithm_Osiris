#import something if you need to.
import h5py
import numpy as np
import os
from os import listdir
import re
import copy

class Individual:
    """
    A class which defines the parameters for each individual.
    The parameters are in a tuple and chosen randomly from a predetermined range.
    The merit is the sum of the individual parameters in this case.
    """

    def __init__(self, *ParameterList):
        self.parameter_list = list(ParameterList)
        self.merit = None
        

    #This method prints the parameters and the merit of each individual when called.
    def __str__(self):
        for i in range(len(self.parameter_list)):
            print(f"p_{i+1}: {self.parameter_list[i]}")
        print(f"Merit: {self.merit}")
        return f""


    #Changes value in input files.
    #Runs the simulation.
    #Extracts the merit.
    #Resets the input file.
    def merit_calc(self, input_file):
        self.change_file(input_file)
        #self.run_simulation()
        #self.extract_merit()
        self.reverse_change(input_file)
        self.merit = sum(self.parameter_list)


    #Reads the file in and changes the appropriate variables.
    def change_file(self, input_file):
        open_file = open(input_file, "rt")
        read_file = open_file.read()
        change1 = read_file.replace('density         = ', f'density         = {self.parameter_list[0]}')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(change1)
        open_file.close()

        open_file = open(input_file, "rt")
        read_file = open_file.read()
        change2 = read_file.replace('per_w0       =  ', f'per_w0       =  {self.parameter_list[1]}')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(change2)
        open_file.close()

        open_file = open(input_file, "rt")
        read_file = open_file.read()
        change3 = read_file.replace('gauss_center(1:2) = ', f'gauss_center(1:2) = {self.parameter_list[2]}')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(change3)
        open_file.close()

        open_file = open(input_file, "rt")
        read_file = open_file.read()
        change4 = read_file.replace('per_focus    =  ', f'per_focus    =  {self.parameter_list[3]}')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(change4)
        open_file.close()


    #This method will run the simulation.
    def run_simulation(self):
        pass

    
    #Puts the data files in a tuple.
    def list_files(self, directory):
        s0 = 'RAW-Beam'
        e0 = '.h5'
        return (f for f in listdir(directory) if (s0 in f and e0 in f))


    #This method will find the merit value.
    def extract_merit(self):
        dirname = 'MS/RAW/Beam'
        files = self.list_files(dirname)
        it_old = 0

        for f in files:
            fullfilename = dirname + '/' + f
            print(fullfilename)
            try:
                it_new = int(re.search('Beam-(.+?).h5', fullfilename).group(1))
                if it_new > it_old:
                    it_old = it_new
                    myfile = fullfilename
            except:
                pass

        hf = h5py.File(myfile,'r')
        #q = hf.get('q').value
        #ene = hf.get('ene').value
        q = np.abs(hf['q'][:])
        ene = hf['ene'][:]

        qene = q * ene
        tot_qene = sum(qene)
        tot_charge = sum(q)
        ave = tot_qene/tot_charge

        variance = np.sqrt(sum(q * (ene - ave)**2/tot_charge))
        self.merit = copy.deepcopy(variance)


    #This reverses the changes so the files can be used agaon for the next gen.
    def reverse_change(self, input_file):
        open_file = open(input_file, "rt")
        read_file = open_file.read()
        reverse1 = read_file.replace(f'density         = {self.parameter_list[0]}', 'density         = ')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(reverse1)
        open_file.close()

        open_file = open(input_file, "rt")
        read_file = open_file.read()
        reverse2 = read_file.replace(f'per_w0       =  {self.parameter_list[1]}', 'per_w0       =  ')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(reverse2)
        open_file.close()

        open_file = open(input_file, "rt")
        read_file = open_file.read()
        reverse3 = read_file.replace(f'gauss_center(1:2) = {self.parameter_list[2]}', 'gauss_center(1:2) = ')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(reverse3)
        open_file.close()

        open_file = open(input_file, "rt")
        read_file = open_file.read()
        reverse4 = read_file.replace(f'per_focus    =  {self.parameter_list[3]}', 'per_focus    =  ')
        open_file.close()
        open_file = open(input_file, "wt")
        open_file.write(reverse4)
        open_file.close()

        
