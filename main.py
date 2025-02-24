# Import elemental libraries
import os
import sys
import numpy as np

# Add the src folder to sys.path stack overflow 
project_root = os.path.abspath(os.path.join('./src'))
print(project_root)
if project_root not in sys.path:
    sys.path.append(project_root)

# Import classes
from channel import Channel
from problem import Problem  
from utils import  *  


channel = Channel(0.7, 1, 0.15, 0.5)

# Define simulation parameters.
n_particles = 500 # Number of particles to simulate
Vx = 0.1 # Initial x-velocity of the particles
Vy = 0.0 # Initial y-velocity of the particles (always 0)

# Initialize the problem with the channel and the number of particles.
problem = Problem(channel, n_particles, Vx, Vy)

# Distribute the particles in the channel.
problem.distribute_initial_particles()

# Run the simulation
problem.run_simulation()

print(f"Flow rate: {problem.compute_particles_flow_rate_interarrival():.2f} particles per second")

# visualize_simulation(out_particles[np.argmax(times_per_particle)], channel, dt_sim=0.15, scale_factor=100)
visualize_simulation_all_particles(problem.channel, problem.particles)


