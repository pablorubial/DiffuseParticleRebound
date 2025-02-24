import numpy as np
class Particle:
    def __init__(self, x, y, Vx, Vy):
        self.x = x # intial x-coordinate of the particles
        self.y = y # initial y-coordinate of the particles
        self.Vx = Vx # x-component of the velocity of the particles at the initial time
        self.Vy = Vy # y-component of the velocity of the particles at the initial time
        self.time = [] # Time taken by the particle to follow each trajectory
        self.trayectory = [(x, y)] # Array of the particle's position
        self.velocities = [(Vx, Vy)] # Array of the particle's velocity at each position
        self.out = False # Boolean variable to check if the particle left the domain
    
    def update_velocity_after_rebound(self, channel, theta):
        # If particle is in the upper part of the conic section
        if (channel.D + channel.d)/2 < self.y < channel.D:
            theta_abs = 3*np.pi/2 - channel.alpha + theta
        # If particle is in the lower part of the conic section
        else:
            theta_abs = np.pi/2 + channel.alpha - theta
        
        V = np.sqrt(self.Vx**2 + self.Vy**2)
        self.Vx = V*np.cos(theta_abs)
        self.Vy = V*np.sin(theta_abs)
        
        self.velocities.append((self.Vx, self.Vy))
    
    def update_position(self, dt):
        self.x += self.Vx*dt
        self.y += self.Vy*dt
        self.trayectory.append((self.x, self.y))
        self.time.append(dt)
    
    def distance_to_conic_section_x(self, channel):
        # Upper part of the conic section
        if (channel.D + channel.d)/2 < self.y < channel.D:
            return channel.l +  (channel.L-channel.l)/((channel.d-channel.D)/2)*(self.y - channel.D)
        # Lower part of the conic section
        elif 1e-16 < self.y < (channel.D - channel.d)/2:
            return channel.l + (channel.L-channel.l)/((channel.D-channel.d)/2)*self.y
        # Not in the conic section automatically left the channel
        else:
            return channel.L
    
    def check_output_condition(self, channel, theta):
        # Upper part of the conic section
        if (channel.D + channel.d)/2 < self.y < channel.D:
            a = np.sqrt((channel.L-self.x)**2 + ((channel.D+channel.d)/2-self.y)**2)
            b = np.sqrt((channel.L-self.x)**2 + ((channel.D-channel.d)/2-self.y)**2) 
        # Lower part of the conic section
        elif 1e-16 < self.y < channel.L:
            a = np.sqrt((channel.L-self.x)**2 + ((channel.D-channel.d)/2-self.y)**2)
            b = np.sqrt((channel.L-self.x)**2 + ((channel.D+channel.d)/2-self.y)**2)

        gamma = np.acos((a**2 + b**2 - channel.d**2)/(2*a*b))
        if theta > (np.pi/2 - gamma):
                return True, gamma
        else:
                return False, gamma
    
    def check_output_time(self, channel):
        return (channel.L - self.x)/self.Vx
        
    def check_rebound_condition_conic_section(self, channel, theta, gamma):
        # Upper part of the conic section
        if (channel.D + channel.d)/2 < self.y < channel.D:
            a = np.sqrt((channel.l-self.x)**2 + (self.y)**2)
            b = np.sqrt((channel.L-self.x)**2 + ((channel.D-channel.d)/2-self.y)**2)
            c = np.sqrt((channel.L-channel.l)**2 + ((channel.D-channel.d)/2)**2)
            xi = np.acos((a**2 + b**2 - c**2)/(2*a*b))
        
        # Lower part of the conic section
        elif 1e-16 < self.y < (channel.D - channel.d)/2:
            a = np.sqrt((channel.l-self.x)**2 + (self.y-channel.D)**2)
            b = np.sqrt((channel.L-self.x)**2 + ((channel.D+channel.d)/2-self.y)**2)
            c = np.sqrt((channel.L-channel.l)**2 + ((channel.D+channel.d)/2-channel.D)**2)
            xi = np.acos((a**2 + b**2 - c**2)/(2*a*b))
        
        if (np.pi/2 - gamma - xi) < theta < (np.pi/2 - gamma):
            return True
        else:
            return False
    
    def check_rebound_time_conic_section(self, channel):
        # Upper part of the conic section
        if (channel.D + channel.d)/2 < self.y < channel.D:
            # Time to reach the lower conic section
            m = (channel.D-channel.d)/(2*(channel.L-channel.l))
            b = -m*channel.l
            return (self.y - m*self.x - b)/(m*self.Vx - self.Vy)
        # Lower part of the conic section
        else:
            # Time to reach the upper conic section
            m = (channel.d-channel.D)/(2*(channel.L-channel.l)) # Slope of the conic section
            b = -m*channel.l + channel.D # y-intercept of the conic section
            return (self.y - m*self.x - b)/(m*self.Vx - self.Vy)
       
    
    def check_rebound_condition_low_plane(self, channel, theta):
        # Lower part of the conic section
        if 1e-16 < self.y < (channel.D - channel.d)/2:
            absolute_theta = np.pi/2 + channel.alpha - theta
            a = np.sqrt(self.x**2 + self.y**2)
            b = np.sqrt((channel.l-self.x)**2 + self.y**2)
            c = channel.l
            xi = np.acos((a**2 + b**2 - c**2)/(2*a*b))
            if np.pi + channel.alpha - xi < absolute_theta < np.pi + channel.alpha :
                return True
            else:
                return False
        # Upper part of the conic section
        else:
            absolute_theta = 3*np.pi/2 - channel.alpha + theta
            a1 = np.sqrt(self.x**2 + self.y**2)
            b1 = np.sqrt((channel.l-self.x)**2 + self.y**2)
            c1 = channel.l
            Gamma = np.acos((a1**2 + b1**2 - c1**2)/(2*a1*b1))
            a2 = np.sqrt((channel.l - self.x)**2 + self.y**2)
            b2 = 2*self.y - channel.D
            c2 = np.sqrt((channel.l - self.x)**2 + (channel.D - self.y)**2)
            epsilon = np.acos((a2**2 + b2**2 - c2**2)/(2*a2*b2))
            if 3*np.pi/2 - epsilon - Gamma < absolute_theta < 3*np.pi/2 - epsilon:
                return True
            else:
                return False
    
    def check_rebound_time_low_plane(self):
        return -self.y/self.Vy
    
    def check_rebound_condition_up_plane(self, channel, theta):
        # Lower part of the conic section
        if 1e-16 < self.y < (channel.D - channel.d)/2:
            absolute_theta = np.pi/2 + channel.alpha - theta
            a1 = np.sqrt(self.x**2 + (channel.D - self.y)**2)
            b1 = np.sqrt((channel.l-self.x)**2 + (channel.D - self.y)**2)
            c1 = channel.l
            Gamma = np.acos((a1**2 + b1**2 - c1**2)/(2*a1*b1))
            a2 = np.sqrt((channel.l - self.x)**2 + (channel.D - self.y)**2)
            b2 =  channel.D - 2*self.y
            c2 = np.sqrt((channel.l - self.x)**2 + self.y**2)
            epsilon = np.acos((a2**2 + b2**2 - c2**2)/(2*a2*b2))
            if np.pi/2 + epsilon < absolute_theta < np.pi/2 + epsilon + Gamma:
                return True
            else:
                return False
           
        # Upper part of the conic section
        else:
            absolute_theta = 3*np.pi/2 - channel.alpha + theta
            a = np.sqrt(self.x**2 + (channel.D - self.y)**2)
            b = np.sqrt((channel.l-self.x)**2 + (channel.D - self.y)**2)
            c = channel.l
            xi = np.acos((a**2 + b**2 - c**2)/(2*a*b))
            if np.pi - channel.alpha < absolute_theta < np.pi - channel.alpha + xi:
                return True
            else:
                return False
    
    def check_rebound_time_up_plane(self, channel):
        return (channel.D - self.y)/self.Vy
    
    def check_rebound_time_inlet(self):
        return -self.x/self.Vx
           
