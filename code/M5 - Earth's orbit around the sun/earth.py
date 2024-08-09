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
M = 1.981e30 #Kg = sun's mass

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