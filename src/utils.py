import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.ticker import MultipleLocator

def interpolate_trayectory(particle, dt_sim=0.25):
    """
    Interpolates a piecewise-linear trayectory based on key particle.trayectory and segment durations.
    """
    traj_segments = []
    t0 = 0.0
    for i in range(len(particle.time)):
        start = np.array(particle.trayectory[i])
        end = np.array(particle.trayectory[i+1])
        T = particle.time[i]
        # Ensure at least 2 points per segment.
        n_frames = max(2, int(np.ceil(T / dt_sim)))
        t_segment = np.linspace(t0, t0 + T, n_frames)
        x_segment = np.linspace(start[0], end[0], n_frames)
        y_segment = np.linspace(start[1], end[1], n_frames)
        seg = np.column_stack((t_segment, x_segment, y_segment))
        traj_segments.append(seg)
        t0 += T
    traj = np.concatenate(traj_segments, axis=0)
    return traj
 
def visualize_simulation_single_particle(particle, channel, dt_sim=0.15, scale_factor=100):
        """
        Animate the trayectory of a single particle..
        """
       
        smooth_traj = interpolate_trayectory(particle, dt_sim=dt_sim)
        
        # Use the channel's visualization method to get figure and axis.
        # Assume channel.visualize(False) returns a valid (fig, ax) tuple.
        fig, ax = channel.visualize(False)
        # Create a marker for the particle.
        particle_marker, = ax.plot([], [], 'bo', markersize=8)
        ax.legend()
        
        def init():
            particle_marker.set_data([], [])
            return (particle_marker,)
        
        def update(frame):
            x, y = smooth_traj[frame, 1], smooth_traj[frame, 2]
            particle_marker.set_data([x], [y])
            return (particle_marker,)
        
        frames = range(len(smooth_traj))
        interval = dt_sim * scale_factor  # Convert simulation seconds to animation ms.
        ani = FuncAnimation(fig, update, frames=frames, init_func=init,
                            blit=True, interval=interval)
        # Save the animation as a GIF using PillowWriter.
        writer = PillowWriter(fps=10) 
        ani.save("./images/simulation.gif", writer=writer)
        print("Animation saved as simulation.gif")
        plt.show()

def visualize_simulation_all_particles(channel, particles):
    """
    Animate the movement of all particles over simulation time T.
    Each particle has its trajectory stored in particle.trayectory and its segment durations in particle.time.
    For particles that finish before T, we hold their final position constant.
    """
    # Define uniform simulation time step.
    T = max([np.sum(p.time) for p in particles]) # Maximum time taken by a particle to leave the domain.
    dt_sim = T / 200  # Time step size for the animation.
    num_frames = int(T / dt_sim)
    
    # Compute a smooth trajectory for each particle.
    smooth_trajs = []
    for p in particles:
        traj = interpolate_trayectory(p, dt_sim=dt_sim)
        smooth_trajs.append(traj)
    
    # Get figure and axis from the channel's visualization method.
    fig, ax = channel.visualize(False)
    
    # Create a marker for each particle.
    markers = []
    for p in particles:
        marker, = ax.plot([], [], 'bo', markersize=4)
        markers.append(marker)
    
    def init():
        for marker in markers:
            marker.set_data([], [])
        return markers
    
    def update(frame):
        # For each particle, update its marker position.
        for i, marker in enumerate(markers):
            traj = smooth_trajs[i]
            # If the particle's trajectory is shorter than the current frame, hold at its final position.
            if frame < traj.shape[0]:
                x, y = traj[frame, 1], traj[frame, 2]
            else:
                x, y = traj[-1, 1], traj[-1, 2]
            marker.set_data([x], [y])
        return markers
    
    ani = FuncAnimation(fig, update, frames=num_frames, init_func=init,
                        blit=True)
    
    # # Optionally, save the animation as a GIF:
    writer = PillowWriter()
    ani.save("./images/all_particles_simulation.gif", writer=writer)
    
    plt.show()


# Function to make high quality plots    
def figure_features(tex=True, font="serif", dpi=180):
    """Customize figure settings.

    Args:
        tex (bool, optional): use LaTeX. Defaults to True.
        font (str, optional): font type. Defaults to "serif".
        dpi (int, optional): dots per inch. Defaults to 180.
    """
    plt.rcParams.update(
        {
            "font.size": 14,
            "font.family": font,
            "text.usetex": tex,
            "figure.subplot.top": 0.9,
            "figure.subplot.right": 0.9,
            "figure.subplot.left": 0.15,
            "figure.subplot.bottom": 0.15,
            "figure.subplot.hspace": 0.2,
            "savefig.dpi": dpi,
            "savefig.format": "pdf",
            "axes.titlesize": 11,
            "axes.labelsize": 11,
            "axes.axisbelow": True,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 5,
            "xtick.minor.size": 2.25,
            "xtick.major.pad": 7.5,
            "xtick.minor.pad": 7.5,
            "ytick.major.pad": 7.5,
            "ytick.minor.pad": 7.5,
            "ytick.major.size": 5,
            "ytick.minor.size": 2.25,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 11,
            "legend.framealpha": 1,
            "figure.titlesize": 16,
            "lines.linewidth": 2,
        }
    )


def add_grid(ax, lines=True, locations=None):
    """Add a grid to the current plot.

    Args:
        ax (Axis): axis object in which to draw the grid.
        lines (bool, optional): add lines to the grid. Defaults to True.
        locations (tuple, optional):
            (xminor, xmajor, yminor, ymajor). Defaults to None.
    """

    if lines:
        ax.grid(lines, alpha=0.5, which="minor", ls=":")
        ax.grid(lines, alpha=0.7, which="major")

    if locations is not None:

        assert (
            len(locations) == 4
        ), "Invalid entry for the locations of the markers"

        xmin, xmaj, ymin, ymaj = locations

        ax.xaxis.set_minor_locator(MultipleLocator(xmin))
        ax.xaxis.set_major_locator(MultipleLocator(xmaj))
        ax.yaxis.set_minor_locator(MultipleLocator(ymin))
        ax.yaxis.set_major_locator(MultipleLocator(ymaj))
