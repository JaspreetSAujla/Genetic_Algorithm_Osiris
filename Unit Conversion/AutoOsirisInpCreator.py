from constitutive_rels import skin_depth
from scipy.constants import e, c, mu_0 as mu0, epsilon_0 as eps0, m_e
import argparse
import numpy as np

if __name__ == "__main__":

    # Specifies how one interacts with the cli options

    parser = argparse.ArgumentParser()
    
    # Filename
    parser.add_argument("-f","--filename", help="specify the file name. Default is output.inp", type=str,default="output.inp")

    # Cores per node

    parser.add_argument("--cores_per_node",type=int,help="the number of cores per node the system will have to work with. Default is 128.",default=128)

    # Dimension

    parser.add_argument("-d","--dimension",type=int,help="the dimension for the simulation to be run in. Default is 2.",choices=[2,3],default=2)

    parser.add_argument("--ndump",default=0,help="specifies the number of iterations between any diagnostic or restart file dumps. Default is 0",type=int)

    # simulation

    simulation = parser.add_argument_group(title="simulation")

    simulation.add_argument("-a","--algorithm",type=str,help="specifies the algorithm to be used in the simulation. Default is 'standard'",default="standard",choices=["standard","quasi_3d","pgc","hd_hybrid"])

    simulation.add_argument("-n0","--plasma_density",type=float,default=0.0,help="specifies the reference simulation plasma density for the simulation in units of [cm^-3].Default is 0.0.")

    # Node number

    node_conf = parser.add_argument_group(title='node_conf')

    node_conf.add_argument("--node_number",type=tuple,help="specifies the number of nodes to use in each direction for the simulation. The total number of nodes will be the product of the number of nodes for each direction. Default is 1.",default=1)

    node_conf.add_argument("--if_periodic",type=tuple,help="specifies if the boundary conditions for each direction will be periodic boundary conditions. Default is false.",default="false")

    # Key values

    parser.add_argument("--laser_wavelength",type=float,help="the wavelength of the laser, in metres",default=8e-7)

    # Window span

    space=parser.add_argument_group(title="space")

    space.add_argument("--boundaries",type=tuple,nargs=2,help="specify the lower and upper boundaries of the global simulation space at the beggining of the simulation in [m]. Default is 0.",default=(0,0))

    space.add_argument("--if_move",type=str,help="pecifies a whether the code should use a moving window at the speed of light in the specified directions. Default is false.",default="false")

    # restart

    restart = parser.add_argument_group(title="restart")

    restart.add_argument("--ndump_fac",default=0,type=int,help="specifies the frequency at which to write restart information. Default is 0.")

    restart.add_argument("--if_restart",default="false",type=str,help="specifies whether the code should attempt to read information from restart files previously saved in order to restart the run exactly as it was at the time the restart information was saved. Default is false.")

    restart.add_argument("--if_remold",default="false",type=str,help="specifies whether the code should remove older restart files after it has successfuly saved restart information on all the nodes. Default is false.")

    # time

    time = parser.add_argument_group(title="time")

    time.add_argument("-t","--time",default=(0,0),type=tuple,help="specify the initial and final time of the simulation in [s]. Default is (0,00).")

    # el_mag_fld

    el_mag_fld = parser.add_argument_group(title="el_mag_fld")

    el_mag_fld.add_argument("--smooth_type",default="none",type=str,help="controls the type of smoothing to be applied to the EM fields. Default is 'none'",choices=["none","stand","local"])

    # emf_bound

    emf_bound = parser.add_argument_group(title="emf_bound")

    emf_bound.add_argument("--emf_type",default=[["vpml"]*2]*2,type=list,help="specifies the boundary conditions to use for the electro-magnetic fields. ### NOT YET FULLY IMPLEMENTED ### Default is [[vpml]*2]*2]")

    emf_bound.add_argument("--emf_smooth_type",default="none",type=tuple,help="specifies the type of smoothing to perform in each direction.")

    # diag_emf [TODO]

    # particles

    particles = parser.add_argument_group(title="particles")

    particles.add_argument("--interpolation",default="quadratic",type=str,help="specifies the interpolation level to be used for all particles. Default is quadratic.")

    # plasma_electrons

    plasma = parser.add_argument_group(title="plasma")

    plasma.add_argument("--num_plasma_e",default=0,type=int,help="specifies the particle buffer size for each node. Default is 0")

    plasma.add_argument("--num_par_x",default=0,type=tuple,help="specifies the number of particles per cell to use in each direction. The total number of particles per cell will be the product of all the components of num_par_x. Default is 0.")

    plasma.add_argument("--plasma_thermal_speed",default=0,type=float,help="specifies the constant thermal spread in velocities for this particle species in each of the directions. Momenta specified are proper velocities i.e. gamma * v in units of c.")

    # beam

    beam = parser.add_argument_group(title="beam")

    beam.add_argument("-q","--beam_charge",default=100e-15,type=float,help="the overall beam charge in [C]. Default is 100fC.")

    beam.add_argument("--num_par_x_beam",default=0,type=tuple,help="specifies the number of particles per cell to use in each direction. The total number of particles per cell will be the product of all the components of num_par_x. Default is 0")
    
    beam.add_argument("--beam_thermal_speed",default=0.0,type=float,help="specifies the constant thermal spread in velocities for this particle species in each of the directions. Momenta specified are proper velocities i.e. gamma * v in units of c. Default is 0.")

    beam.add_argument("-E","--beam_energy",type=float,default=50,help="specifies the energy of the injected beam, in [MeV]. Default is 50MeV")

    beam.add_argument("--beam_density",default=4.26e21,type=float,help="the density of the beam in /m^3")

    # laser

    laser = parser.add_argument_group(title="laser")

    laser.add_argument("-I","--intensity",default=0,type=float,help="specify the peak laser intensity in [W * cm^-2]")

    # currents

    current = parser.add_argument_group(title="current")

    current.add_argument("--current_smooth_type",default="none",type=tuple,help="specifies the type of smoothing to perform in each direction")

    # Only run this at the end
    args = parser.parse_args()

    with open(args.filename,"w+") as file:

        # simulation

        file.write("simulation\n{\n")

        file.write(f"algorithm = '{args.algorithm}',\n")

        file.write(f"n0 = {args.plasma_density}, ! [cm^-3] \n")

        file.write("}\n")

        # node_conf

        file.write("\nnode_conf\n{\n")

        file.write(f"node_number(1:{args.dimension}) = " + str(args.node_number).replace("(","").replace(")","") + ",\n")

        file.write(f"if_periodic(1:{args.dimension}) = " + str(args.if_periodic).replace("(",".").replace(")",".").replace(",",".,.").replace("'","").replace(" ","") + ",\n}\n") # broken

        # spatial grid
        file.write("\ngrid\n{\n")

        delta1 = args.laser_wavelength / (20 * skin_depth(args.plasma_density)) # x

        delta2 = 1 / 4 #y

        delta3 = 1 / 4 #z

        window_lengths = args.boundaries

        for count,item in enumerate(args.boundaries): # Jesus that's a lot. Essentially, I want to take the user's two input tuples (e.g. 0,0,0 1,2,3), and take their difference into a list or tuple. Please submit a commit if you can fix this to be shorter.
            dummyString = ""

            for subitem in item:

                dummyString += subitem

            window_lengths[count] = [float(i) for i in dummyString.split(",")]

        boundaries = [list(map(lambda x: x/skin_depth(args.plasma_density),i) )for i in window_lengths]

        window_lengths = [abs(window_lengths[1][i] - window_lengths[0][i]) for i in range(args.dimension)]

        window_lengths = [i / skin_depth(args.plasma_density) for i in window_lengths]

        # nx, ny, nz

        nx = int(np.ceil(

            np.ceil(
                window_lengths[0] / delta1

            )/args.cores_per_node
        )*args.cores_per_node)

        ny = int(np.ceil(

            np.ceil(
                window_lengths[1] / delta2

            )/args.cores_per_node
        )*args.cores_per_node)
        try: # skips nz if it's only 2D
            nz = int(np.ceil(

            np.ceil(
                window_lengths[2] / delta3

            )/args.cores_per_node
        )*args.cores_per_node)

            nlist = [nx,ny,nz]
        except:
            nlist = [nx,ny]
            pass

        
        file.write(f"nx_p(1:{args.dimension}) = " + str(nlist).replace("[","").replace("]","") + ",\n")

        file.write("}\n")

        # Time-step

        file.write("\ntime_step\n{\n")

        file.write(f"dt = {1 / np.sqrt(2*sum(map(lambda x: 1/(x*x),[delta1,delta2]))) if args.dimension == 2 else 1 / np.sqrt(2*sum(map(lambda x: 1/(x*x),[delta1,delta2,delta3])))}, ! courant condition /sqrt(2) \n")

        file.write(f"ndump = {args.ndump},\n")

        file.write("}\n")

        # Restart

        file.write("\nrestart\n{\n")

        file.write(f"ndump_fac = {args.ndump_fac},\n")
        file.write(f"if_restart = .{args.if_restart}.,\n")
        file.write(f"if_remold = .{args.if_remold}.,\n")

        file.write("}\n")

        # Space

        file.write("\nspace\n{\n")

        file.write(f"xmin(1:{args.dimension}) = " + str(boundaries[0]).replace("[","").replace("]",",\n"))

        file.write(f"xmax(1:{args.dimension}) = " + str(boundaries[1]).replace("[","").replace("]",",\n"))

        file.write(f"if_move(1:{args.dimension}) =  " + f"{args.if_move}".replace("(",".").replace(")",".").replace(",",".,.").replace("'","").replace(" ","") + ",\n}\n") # broken

        # time

        file.write("\ntime\n{\n")

        file.write(f"tmin = {args.time[0] / skin_depth(args.plasma_density)},\n")
        file.write(f"tmax = {args.time[1]/ skin_depth(args.plasma_density)},\n")

        file.write("}\n")

        # el_mag_fld

        file.write("\nel_mag_fld\n{\n")

        file.write(f'smooth_type = "{args.smooth_type}",\n')

        file.write("}\n")

        # emf_bound

        file.write("\nemf_bound\n{\n")

        for i in range(args.dimension):
            file.write(f"type(1:{args.dimension},{i+1}) = {args.emf_type[i]}".replace("[","").replace("]","").replace("'",'"') + ",\n")

        file.write("}\n")

        file.write("\nsmooth\n{\n")

        file.write(f"type(1:{args.dimension}) =  {args.emf_smooth_type},\n".replace("', '","").replace("('","").replace("')",""))

        file.write("}\n")

        # diag_emf

        # Jees this is a lot, come back to this [TODO]

        # particles

        file.write("\nparticles\n{\n")

        file.write("num_species = 2,\n")

        file.write("num_cathode= 0,\n")

        file.write(f'interpolation = "{args.interpolation}",\n')

        file.write("}\n")

        # plasma electrons

        file.write("\nspecies\n{\n")

        file.write('name = "electrons",\n')

        file.write(f"num_par_max = {args.num_plasma_e},\n")

        file.write("rqm = -1.0d0,\n")

        file.write(f"num_par_x(1:{args.dimension}) = " + str(args.num_par_x).replace("(","").replace(")","") + ",\n")

        file.write("}\n")

        file.write("\nudist\n{\n")

        file.write(f"uth(1:3) = {args.plasma_thermal_speed}, {args.plasma_thermal_speed}, {args.plasma_thermal_speed},\n")

        file.write("ufl(1:3) = 0.0, 0.0, 0.0,\n")

        file.write("}\n")

        file.write("\nprofile\n{\n")

        file.write("density = 1.0,\n")

        file.write('profile_type = "math_func",\n')

        file.write('math_func_expr = ,\n') #[TODO]

        file.write("}\n")

        # need spe_bound and diag_species

        # beam electrons, real s**t

        file.write("\nspecies\n{\n")

        file.write('name = "Beam",\n')

        file.write(f"num_par_max = {int(args.beam_charge / e)},\n")

        file.write("rqm = -1.0d0,\n")

        file.write(f"num_par_x(1:{args.dimension}) = " + str(args.num_par_x_beam).replace("(","").replace(")","") + ",\n")

        file.write("init_fields = .true.,\n")

        file.write("}\n")

        file.write("\nudist\n{\n")

        file.write(f"uth(1:3) = {args.beam_thermal_speed}, {args.beam_thermal_speed}, {args.beam_thermal_speed},\n")

        file.write(f"ufl(1:3) = {args.beam_energy * e * 1e6 / (m_e * c * c)}, 0, 0,\n")

        file.write("}\n")

        file.write("\nprofile\n{\n")

        file.write(f"density = {args.beam_density / args.plasma_density},\n")

        # profile for profile

        file.write("}\n")

        # spe_bound, and diag_species

        # zpulse

        file.write("\nzpulse\n{\n")

        file.write(f"a0 = { (e/(np.pi * m_e * np.sqrt(2*eps0 * c ** 5 ))) *  np.sqrt(args.intensity * 1e4) * args.laser_wavelength},\n")

        file.write(f"omega0 = {2 * np.pi * c * np.sqrt(eps0 * m_e / args.plasma_density) / (args.laser_wavelength * e)},\n")

        file.write("pol = 0.0,\n")

        file.write("pol_type = 0,\n")

        file.write('propagation = "forward",\n')

        file.write("}\n")

        file.write("\nsmooth\n{\n")

        file.write(f"type(1:{args.dimension}) = {args.current_smooth_type},\n")

        file.write("}\n")





