import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from diffuse import Diffuse
from particles import Particle

class Problem:
    def __init__(self, channel, n_particles, Vx, Vy, tol=0.01):
        """
        Initialize the simulation with a computational domain (channel) and a number of particles.
        """
        self.channel = channel # Channel object
        self.n_particles = n_particles # Number of particles to simulate
        self.Vx = Vx # Initial x-velocity of the particles
        self.Vy = Vy # Initial y-velocity of the particles
        self.tol = tol # Tolerance for initial y positions to do not have particles very close to the walls.
        self.particles = [] # List of Particle objects
        self.count = 0 # Number of particles that left the domain.
    
    def distribute_initial_particles(self):
        """
        Generate particles with x = 0 and uniformly distributed y positions.
        """
        for i in range(self.n_particles):
            y_init = np.random.uniform(self.tol, self.channel.D - self.tol)
            # Assuming Particle constructor: Particle(id, x, y, Vx, Vy)
            p = Particle(i, 0, y_init, self.Vx, self.Vy)
            self.particles.append(p)
    
    def simulate_particle(self, particle):
        """
        Run simulation for single particle.
        """
        # Compute the distance to the conic section
        d1 = particle.distance_to_conic_section_x(self.channel)
        # Automatically particle left the channel
        if np.abs(d1 - self.channel.L) < 1e-16:
            # Particle lelave the domain
            time = (d1)/particle.Vx
            particle.update_position(time)
            self.count += 1
            particle.out = True
        else:
            # Compute time taken to reach the conic section
            time = d1/particle.Vx
            particle.update_position(time)
            # Rebound with the conic section
            theta = Diffuse.sample_angle()
            flag, gamma = particle.check_output_condition(self.channel, theta)
            if flag:
                particle.update_velocity_after_rebound(self.channel, theta)
                dt = particle.check_output_time(self.channel)
                particle.update_position(dt)
                self.count += 1
                particle.out = True
            else:
                while particle.check_rebound_condition_conic_section(self.channel, theta, gamma):
                    particle.update_velocity_after_rebound(self.channel, theta)
                    dt = particle.check_rebound_time_conic_section(self.channel)
                    particle.update_position(dt)
                    theta = Diffuse.sample_angle()
                    flag, gamma = particle.check_output_condition(self.channel, theta)
                    if flag:
                        particle.update_velocity_after_rebound(self.channel, theta)
                        dt = particle.check_output_time(self.channel)
                        particle.update_position(dt)
                        self.count += 1
                        particle.out = True
                        break
                
                if not particle.out:
                    if particle.check_rebound_condition_low_plane(self.channel, theta):
                        particle.update_velocity_after_rebound(self.channel, theta)
                        dt = particle.check_rebound_time_low_plane()
                        particle.update_position(dt)
                    elif particle.check_rebound_condition_up_plane(self.channel, theta):
                        particle.update_velocity_after_rebound(self.channel, theta)
                        dt = particle.check_rebound_time_up_plane(self.channel)
                        particle.update_position(dt)
                    else:
                        # Particle reaches the inlet
                        particle.update_velocity_after_rebound(self.channel, theta)
                        dt = particle.check_rebound_time_inlet()
                        particle.update_position(dt)

    
    def run_simulation(self):
        """
        Run the simulation for each particle.
        """
        print("Running simulation with {} particles...".format(self.n_particles))
        for particle in self.particles:
            self.simulate_particle(particle)
        print("Simulation finished.")
    
    def compute_particles_flow_rate_interarrival(self):
        """
        Compute the flow rate of particles leaving the domain using the interarriva time method.
        """
        out_particles = [p for p in self.particles if p.out]
        times_per_particle = [np.sum(p.time) for p in out_particles]
        sorted_exit_times = np.sort(times_per_particle)
        inter_arrival_times = np.diff(sorted_exit_times)
        mean_interarrival = np.mean(inter_arrival_times)
        flow_rate = 1 / mean_interarrival
        return flow_rate
    
    def compute_particles_flow_max_time(self):
        """
        Compute the flow rate of particles leaving the domain using the maximum time method.
        """
        out_particles = [p for p in self.particles if p.out]
        times_per_particle = [np.sum(p.time) for p in out_particles]
        return self.count/np.max(times_per_particle)
    
