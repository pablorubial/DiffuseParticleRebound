import numpy as np
# Diffuse model based on Knusden cosine law. This model can be changed as desired by the user.
class Diffuse:
    @staticmethod
    def sample_angle():
        # Inverse transform sampling: u in [0,1] gives alpha = arcsin(2u - 1)
        u = np.random.rand()
        return np.arcsin(2*u - 1) # Return a value between -pi/2 and pi/2