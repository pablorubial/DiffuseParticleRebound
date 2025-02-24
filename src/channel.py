import numpy as np
import matplotlib.pyplot as plt
from utils import figure_features

class Channel:
    def __init__(self, l, L, d, D):
        self.l = l # Starting of the conical section
        self.L = L # Length of the channel
        self.d = d # Diameter of the outlet
        self.D = D # Diameter of te channel
        self.alpha = np.arctan((D-d)/2/(L-l)) # Opening angle of the conical section (needed to compute absolute angles)
            
    def visualize(self, visualize=False):
        # For LaTeX labels rendering
        figure_features()
        
        # Figure
        fig, ax = plt.subplots()
        ax.plot([0, self.l], [0, 0], color='k', linewidth=2)
        ax.plot([self.l, self.L], [0, (self.D-self.d)/2], color='k', linewidth=2)
        ax.plot([self.L, self.L], [(self.D-self.d)/2, (self.D+self.d)/2], color='k', linewidth=2)
        ax.plot([self.L, self.l], [(self.D+self.d)/2, self.D], color='k', linewidth=2)
        ax.plot([self.l, 0], [self.D, self.D], color='k', linewidth=2)
        ax.plot([0, 0], [self.D, 0], color='k', linewidth=2)

        # Labels
        plt.xlabel(r'$x$')
        plt.ylabel(r'$y$')
        
        # If a quick visualization is needed
        if visualize:
            plt.show()
        # To make the figure available for further animation
        else:
            return fig, ax