# Libraries
import pygame as pg
import math
from random import randint
import numpy as np

# Initialize Pygame
pg.init()

# Create window 
screen_info = pg.display.Info()
WIDTH = screen_info.current_w - 10
HEIGHT = screen_info.current_h - 10
WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Solar System Simulator')


#define colors for simulation
#WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GRAY = (128,128,128)
YELLOWISH_WHITE = (255,255,246)
BLUE = (0,0,255)
RED = (188,39,50)
NAME_TEXT_COLOR=(111,236,123)
DIST_TEXT_COLOR=(56,190,255)
SUN_NAME_COLOR=(144,128,254)
SUN_TEXT_COLOR=(54,32,12)
# font set up
NAME_TEXT=pg.font.SysFont(name='TimesRoman', size = 18, bold=True)
DIST_TEXT= pg.font.SysFont(name='Sans', size=18, bold=True)



# Class Solar System Bodies
class SolarSystemBodies:
     
     #astronomical unit = distance from Sun to Earth
     AU = 1.496e11
     SCALE = 230/AU
     G = 6.6743e-11
     dt = 24*3600 #seconds in a day
     
     
     def __init__(self, name, color, x,y, mass, radius):
          self.name = name
          self.color = color
          self.x = x
          self.y = y
          self.mass = mass
          self.radius = radius
          self.x_vel = 0
          self.y_vel = 0
          self.orbit = []
          self.sun = False
          self.distance_to_sun = 0
          self.r = [(self.x,self.y)]
          self.a_list = []
          
          #self.acc = 0
    
    # Method 1: draw bodies on the simulator
     def draw_body(self, WINDOW):
        x = self.x*SolarSystemBodies.SCALE + WIDTH//2
        y = self.y*SolarSystemBodies.SCALE + HEIGHT//2
        pg.draw.circle(surface = WINDOW, color = self.color, center=(x,y), radius = self.radius )
        
        
        if not self.sun: # -> if self.sun==False
            name_text=NAME_TEXT.render(self.name, True, NAME_TEXT_COLOR)
            WINDOW.blit(name_text,(x-40,y-55))
            dist_text = DIST_TEXT.render(f"{round(self.distance_to_sun/(3e8*60), 3)} lt-min", True, DIST_TEXT_COLOR)
            WINDOW.blit(dist_text,(x-40,y-35))
        else:
             name_text=NAME_TEXT.render(self.name, True, SUN_NAME_COLOR)
             WINDOW.blit(name_text,(x-40,y-55))
             dist_text = DIST_TEXT.render(f"{round(self.x/3e8, 3), round(self.y/3e8, 3)} lt-sec", True, DIST_TEXT_COLOR)
             WINDOW.blit(dist_text,(x-40,y-35))
             
      
     def acceleration(self, ss_body):
          G=6.6743e-11
          r = np.array([self.x,self.y])
          r_size =np.linalg.norm(r)
          
        
          if r_size == 0:  # evitare divisione per zero
            return 0, 0
        
          # Calcolo dell'accelerazione
          a = G * ss_body.mass / r_size**2
          #print("HERE ", a)
          # Direzione dell'accelerazione
          a_x = a * r[0] / r_size
          a_y = a * r[1] / r_size

          if ss_body.sun:
               self.distance_to_sun = r_size
               
          return a_x, a_y

     def acceleration2(self, ss_body):
          G=6.6743e-11
          x_diff = ss_body.x - self.x 
          y_diff = ss_body.y - self.y
          r = np.array([self.x,self.y])
          r_size = np.linalg.norm(r)

          if r_size == 0:  # evitare divisione per zero
            return 0, 0
          a_vector =  (G * ss_body.mass / r_size**3) * r
          
          a_x = a_vector[0] 
          a_y = a_vector[1]

          if ss_body.sun:
               self.distance_to_sun = r_size
          return a_x, a_y 
          


     # Method 3: update position
     def update_position2(self, ss_bodies):
          a = np.array([0.0,0.0])  # Reset dell'accelerazione ad ogni ciclo di aggiornamento

          for ss_body in ss_bodies:
               if self != ss_body:  # Evita di calcolare la propria attrazione gravitazionale
                    #print("calcualting effect of ",ss_body.name, " on ", self.name)
                    #dist = np.array([ss_body.x - self.x, ss_body.y - self.y])
                    r = np.array([self.x,self.y])
                    
                    net_fx,net_fy= self.acceleration2(ss_body)
                    #print("QUI", net_fx)
                    a[0]+= net_fx
                    a[1]+=net_fy
                    #net_fx+=a_x
                    #net_fy+=a_y
                    
               
          
          # Aggiorna la velocità e la posizione
          self.x_vel += self.dt * a[0]  # componente x dell'accelerazione
          self.y_vel += self.dt * a[1]  # componente y dell'accelerazione
          
          self.x += self.x_vel * self.dt
          self.y += self.y_vel * self.dt


          self.orbit.append((self.x, self.y))

     # Method 3: update position
     def update_position3(self, ss_bodies):
          net_fx, net_fy = 0,0

          for ss_body in ss_bodies:
               if self != ss_body:  # Evita di calcolare la propria attrazione gravitazionale
                    print("calcualting effect of ",ss_body.name, " on ", self.name)
                    #dist = np.array([ss_body.x - self.x, ss_body.y - self.y])
                    #r = np.array([self.x,self.y])
                    f_x,f_y = self.acceleration(ss_body)
                    #print(f_x, f_y)
                    net_fx+=f_x
                    net_fy+=f_y
                    
                    
                    if ss_body.sun:
                         self.distance_to_sun = np.linalg.norm(r)
          
          # Memorizza l'accelerazione corrente
          #self.a_list.append(self.acc)
          
          
          # Aggiorna la velocità e la posizione
          self.x_vel += self.dt * net_fx  # componente x dell'accelerazione
          self.y_vel += self.dt * net_fy  # componente y dell'accelerazione
          #print("VELOCITY ", self.x_vel, self.y_vel)
          self.x += self.x_vel * self.dt
          self.y += self.y_vel * self.dt


          self.orbit.append((self.x, self.y))
          

     # Method 4 - ttack orbit
     def track_orbit(self, WINDOW):
          if len(self.orbit) > 1:
               centered_points = []
               for (x,y) in self.orbit:
                    #center and scale coordinates
                    x = x*SolarSystemBodies.SCALE + WIDTH//2
                    y = y*SolarSystemBodies.SCALE + HEIGHT//2
                    centered_points.append((x,y))

               pg.draw.lines(surface=WINDOW, color=self.color, closed=False, points = centered_points, width=2)

     # Method 5 - combine draw_body and track_orbit in one function
     def draw(self, WINDOW, track=True):
          self.draw_body(WINDOW)
          if track:
               self.track_orbit(WINDOW)
              



# Stars list with color, center and radius
star_list = [{'color': (randint(190,255), randint(190,255), randint(190,255)),
               'center': (randint(5, WIDTH), randint(5, HEIGHT)),
               'radius': (randint(1,2))
               }
            for star in range(450)]


# Function to draw stars in teh background
def draw_stars(stars_list):
     for star in stars_list:
          pg.draw.circle(WINDOW, star['color'], star['center'], star['radius'])




#create simulation
run = True
paused=False
# Bodies
sun = SolarSystemBodies("Sun", YELLOW, 0, 0.0, 1.989e30, 30)
sun.sun=True
#sun.x_vel = 0.004589483670395888
#sun.y_vel = 0.0
mercury = SolarSystemBodies("Mercury", GRAY, 0.39*SolarSystemBodies.AU, 0, 0.33e24, 6)
mercury.y_vel = -47.4e3
venus = SolarSystemBodies("Venus", YELLOWISH_WHITE, 0.72*SolarSystemBodies.AU, 0, 4.87e24, 14)
venus.y_vel = -35e3
earth = SolarSystemBodies("Earth", BLUE, SolarSystemBodies.AU, 0, 5.97e24, 15)
earth.y_vel = -29.8e3
mars = SolarSystemBodies("Mars", RED, 1.52*SolarSystemBodies.AU, 0, 0.642e24, 8)
mars.y_vel = -24.1e3

# Set FPS for simulation
FPS = 60
clock = pg.time.Clock()

while run:
    WINDOW.fill(BLACK)
    clock.tick(FPS)
    draw_stars(star_list)
    #print(star_list)
    for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                 if event.key == pg.K_ESCAPE:
                      run = False
                 elif event.key == pg.K_SPACE:
                      paused = not paused

    if not paused:         
     ss_bodies = [sun, mercury, venus, earth, mars]
     
     for body in ss_bodies:
          #print("Iteration for ",body.name,"***************************")
          body.update_position2(ss_bodies)
          body.draw(WINDOW)
          
     print("SUN",sun.orbit)
     print("VENUS",venus.orbit)
     print("EARTH",earth.orbit)
     
          

     pg.display.update()
    



    
# quit pygame
pg.quit()


    