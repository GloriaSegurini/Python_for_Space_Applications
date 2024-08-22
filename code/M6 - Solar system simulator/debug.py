
import math
from random import randint




# Class Solar System Bodies
class SolarSystemBodies:
     
     #astronomical unit = distance from Sun to Earth
     AU = 1.496e11
     G = 6.6743e-11
     dt = 24*3600 #seconds in a day
     
     def __init__(self, name, x,y, mass, radius):
          self.name = name
          
          self.x = x
          self.y = y
          self.mass = mass
          self.radius = radius
          self.x_vel = 0
          self.y_vel = 0
          self.orbit = []
          self.sun = False
          self.distance_to_sun = 0
    
    # Method 1: draw bodies on the simulator
     def draw_body(self):
        x = self.x
        y = self.y
        #pg.draw.circle(surface = WINDOW, color = self.color, center=(x,y), radius = self.radius )

    # Method 2: calculate the gravitational force
     def gravitational_force(self, ss_body):
        # F = GMm/r^2

        x_diff = ss_body.x - self.x 
        print(ss_body.name, ss_body.x)
        y_diff = ss_body.y - self.y
        print("y_diff",y_diff)
        print("x_diff",x_diff)
        distance = math.sqrt(x_diff**2 + y_diff**2) #take euclidean distance
        print("distance",distance)
        if ss_body.sun:
             self.distance_to_sun = distance
        g_force = self.G * self.mass * ss_body.mass / distance**2
        print("g_force",g_force)

        # calculating g_force gives the force's magnitude, not its direction. We must treat it as a vectorial quantity
        theta = math.atan2(y_diff,x_diff)
        print("theta",theta)
        f_x = g_force * math.cos(theta)
        f_y = g_force * math.sin(theta)

        if self.name=="Mercury":
            print("QUI",f_x,f_y)
        return f_x, f_y 
     
     # Method 3: update position
     def update_position(self, ss_bodies):
          net_fx, net_fy = 0,0
          print(self.name, "'s initial velocity",self.x_vel, self.y_vel)
          print(self.name, "'s initial position",self.x, self.y)
          #print(self.x,self.y)
          for body in ss_bodies:
               #print("HERE1, self is",self.name)
               if self != body:
                    print("Calculating the effect of ", body.name, " on ", self.name)
                    f_x, f_y = self.gravitational_force(body)
                    net_fx+= f_x
                    net_fy+=f_y
          
          self.x_vel+=net_fx/self.mass*self.dt
          self.y_vel+=net_fy/self.mass*self.dt
          
          self.x+=self.x_vel*self.dt
          self.y+=self.y_vel*self.dt
          print(self.name, "'s final velocity",self.x_vel, self.y_vel)
          print(self.name, "'s final position",self.x, self.y)
          
          self.orbit.append((self.x,self.y))

          #print(self.name, self.x, self.y)
        

# Bodies
sun = SolarSystemBodies("Sun",  0,0, 1.989e30, 30)
sun.sun = True
mercury = SolarSystemBodies("Mercury",  0.39*SolarSystemBodies.AU, 0, 0.33e24, 6)
mercury.y_vel = -47.4e3
venus = SolarSystemBodies("Venus",  0.72*SolarSystemBodies.AU, 0, 4.87e24, 14)
venus.y_vel = -35e3
earth = SolarSystemBodies("Earth", SolarSystemBodies.AU, 0, 5.97e24, 15)
earth.y_vel = -29.8e3
mars = SolarSystemBodies("Mars",  1.52*SolarSystemBodies.AU, 0, 0.642e24, 8)
mars.y_vel = -24.1e3


ss_bodies = [sun, mercury, venus, earth, mars]

for i in range(3):
    print("Iteration ",i,"*********************************************************************")
    for body in ss_bodies:
        print("ITERATION FOR ", body.name, "******************")
        body.update_position(ss_bodies)
        body.draw_body()

    
   
    