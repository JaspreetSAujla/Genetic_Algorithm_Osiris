import json
import math

"""
Takes an input file of system parameters, and converts them to usable relative numbers.
"""

# Bring data in

with open("inputs.json", "r") as read_file:
    data = json.load(read_file)

# Creates dictionaries from the data

for meta_config in data:

    dummy = str(meta_config)

    # This creates the dictionaries, so any undefined errors are resolved by
    # this

    exec(dummy + " = " + str(data[str(meta_config)]))

# Constants

# Taken from CODATA

e = 1.602176634e-19  # C, elementary charge
c = 299792458  # m/s, speed of light in vacuo
eps0 = 8.8541878128e-12  # F/m, vacuum electric permittivity
mu0 = 1.25663706212e-6  # N/(A*A). vacuum magnetic permeability
m_e = 9.1093837015e-31  # kg, electron mass

# Calculates the SI values

# Plasma

uniform_length = Plasma['total_length'] - (sum(Plasma['ramp_lengths']))
frequency = math.sqrt((Plasma['density'] * e * e) / (eps0 * m_e))
wavelength = 2 * math.pi * c / frequency
period = wavelength / c
skin_depth = c / frequency

# Laser

frequency = 2 * math.pi * c / Laser['wavelength']

# Witness Beam

num_electrons = Witness_Beam['charge'] / e


# System

x_step = Laser['wavelength'] / 20
y_step = skin_depth / 4
z_step = skin_depth / 4

nx = System['window_dimensions'][0] / x_step
ny = System['window_dimensions'][1] / y_step
nz = System['window_dimensions'][2] / z_step

dt = 0.99 * (math.sqrt(x_step**2 + y_step**2 + z_step**2) / c)

print(dt)
