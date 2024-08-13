'''
Problem Statement
-----------------
- Create a simulation to track the orbit of the Earth around the Sun for a period of 1 year
- Use Euler and Runge - Kutta method of 4th order for this task
- Find the distance from Earth to Sun at Apogee using Euler and RK4 method and comapre it with th original

Given Equations
-----------------
Acceleration of Earth due to Gravity of the Sun  
--> a = (_GM / |r|^3)*r_vec
G = universal gravitational cosntant
M = mass of the Sun
r = distance Sun-Earth at a given point
r_vec = vector that is facing from the Earth towards the sun


ODE (ordinary differential equation) for Position
-> dr/dt = v
velocity is the rate of change at position r

ODE for Velocity
-> dv/dt = a

Initial Condition
-----------------
-> Earth is at its Perihelion (closest to Sun)
'''

# Imports
import matplotlib.pyplot as plt
import numpy as np


# Constants
G = 6.6743e-11
M = 1.989e30 #Kg = sun's mass

# Initial Position and Velocity
r_0 = np.array([147.1e9,0]) #m, Perihelion
v_0 = np.array([0, -30.29e3]) #m/s, Earth's velocity at Perihelion

# Time steps and total time for simulation
dt = 3600 #s, after how many seconds we are going to update our simulation
t_max = 3.154e7 #seconds in a year


# # Time array to be used in numerical solution
t = np.arange(0, t_max, dt)
#print(t.astype('int32'))

#  Initialize arrays to store positions and velocities at all time steps
r = np.empty(shape=(len(t),2))
v = np.empty(shape=(len(t),2))

# Set initial conditions for position and velocity
r[0], v[0] = r_0, v_0

# Choosing the numerical integration method
method_integration = 'rk4'

# Define a function that returns the acceleration vector of a given body when passed into the position vector

def accn(r):
    r_size = np.linalg.norm(r)
    return (-G*M / r_size**3)*r

# Euler Integration
def euler(r,v,accn,dt):
    # objective: update empty arrays for r,v  with the simulated data
    '''
    ODE (ordinary differential equation) for Position
    -> dr/dt = v
    velocity is the rate of change at position r
    -> r_new = r_old + v_old*dt

    
    ODE for Velocity
    -> dv/dt = a
    -> n_new = v_old + a(r_old)*dt
    '''

    for i in range(1, len(t)): #not 0, because we already have the initial vetors fo r and v
        r[i] = r[i-1] + v[i-1]*dt
        v[i] = v[i-1] + accn(r[i-1])*dt


# RK Integration
def rk4(r,v,accn,dt):
    '''
    Step 1:
    k1v = accn(r[i-1])
    k1r = v[i-1]

    Step 2: dt/2 using k1
    k2v = accn(r[i-1] + k1r * dt/2)
    k2r = v[i-1] + k1v*dt/2

    Step 3: dt/2 using k2
    k3v = accn(r[i-1] + k2r * dt/2)
    k3r = v[i-1] * k2v * dt/2

    Step 4: dt using k3
    k4v = accn(r[i-1 + k3v*dt])
    k4r = v[i-1] + k3v * dt
    '''
    
    for i in range(1,len(t)):
        
        k1v = accn(r[i-1])
        k1r = v[i-1]

        
        k2v = accn(r[i-1] + k1r * dt/2)
        k2r = v[i-1] + k1v*dt/2

        k3v = accn(r[i-1] + k2r * dt/2)
        k3r = v[i-1] + k2v * dt/2

        
        k4v = accn(r[i-1] + k3r*dt)
        k4r = v[i-1] + k3v * dt

        # Update r and v
        v[i] = v[i-1] + dt/6*(k1v+2*k2v+2*k3v+k4v)
        r[i] = r[i-1] + dt/6*(k1r+2*k2r+2*k3r+k4r)



def numerical_integration(r,v,accn,dt, method):
    if method=='euler':
        euler(r,v,accn,dt)
    elif method =='rk4':
        rk4(r,v,accn,dt)
    else:
        raise Exception('You can either choose "euler" or "rk4" method')
    


numerical_integration(r,v,accn,dt,method = method_integration)

# Apply
sizes = [np.linalg.norm(position) for position in r]
pos_aphelion = np.max(sizes)
arg_aphelion = np.argmax(sizes)
vel_aphelion = np.linalg.norm(v[arg_aphelion])

#print(r)
print("pos_aphelion: ", pos_aphelion/1e9, "vel_aphelion: ",vel_aphelion/1e3)
#print(r)






'''
# Calcolo delle derivate numeriche dx/dt e dy/dt
dx_dt = np.diff(r[:,0]) / dt  # Derivata numerica di x rispetto al tempo
dy_dt = np.diff(r[:,1]) / dt  # Derivata numerica di y rispetto al tempo

# Calcolo della velocità scalare usando la norma delle derivate
vel_numerical = np.sqrt(dx_dt**2 + dy_dt**2)

# Confronto tra la velocità scalare calcolata direttamente e quella calcolata con le derivate
vel_aphelion_numerical = vel_numerical[arg_aphelion-1]  # Nota: np.diff riduce la dimensione di 1
vel_aphelion_direct = np.linalg.norm(v[arg_aphelion])

print(f"Velocità all'afelio usando la norma di (dx/dt, dy/dt): {vel_aphelion_numerical}")
print(f"Velocità all'afelio calcolata direttamente: {vel_aphelion_direct}")
'''

# Plotting the simulated data on 3D axis
plt.style.use('dark_background')
plt.figure(figsize = (7,12))
plt.subplot(projection='3d')
suptitle_str = 'RK4' if method_integration == 'rk4' else 'Euler'
plt.title(f"""At Aphelion, the Earth is {round(pos_aphelion/1e9, 1)} million kms 
away from the Sun\nMoving at the speed of {round(vel_aphelion/1e3,1)} km/s.""", fontsize=14, color = 'orange')
plt.suptitle(suptitle_str + ' Method', fontsize = 18, weight = 'bold')
plt.plot(r[:,0], r[:,1], color = 'tab:pink', lw = 2, label = "Earth's Orbit")
plt.scatter(0,0, color = 'yellow', s= 1000, label = 'sun') #sun
plt.scatter(r[0,0], r[0,1], s = 200, label = 'Earth at its Perihelion')
plt.scatter(r[arg_aphelion,0], r[arg_aphelion,1], s = 200, label = 'Earth at its Aphelion', color = 'blue')
legend = plt.legend(loc='lower right', frameon = False)
legend.legend_handles[1]._sizes = [150]
legend.legend_handles[2]._sizes = [80]
plt.axis('off')
plt.show()

