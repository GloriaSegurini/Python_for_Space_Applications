# Libraries
import pygame as pg
import math
from random import randint

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
             
          


    # Method 2: calculate the gravitational force
     def gravitational_force(self, ss_body):
        # F = GMm/r^2

        x_diff = ss_body.x - self.x 
        y_diff = ss_body.y - self.y
        distance = math.sqrt(x_diff**2 + y_diff**2) #take euclidean distance
        if ss_body.sun:
             self.distance_to_sun = distance
     
        g_force = self.G * self.mass * ss_body.mass / distance**2

        # calculating g_force gives the force's magnitude, not its direction. We must treat it as a vectorial quantity
        theta = math.atan2(y_diff,x_diff)
        f_x = g_force * math.cos(theta)
        f_y = g_force * math.sin(theta)
        return f_x, f_y 
     
     # Method 3: update position
     def update_position(self, ss_bodies):
          net_fx, net_fy = 0,0
          for body in ss_bodies:
               #print(body)
               if self != body:
                    f_x, f_y = self.gravitational_force(body)
                    net_fx+= f_x
                    net_fy+=f_y
          
          self.x_vel+=net_fx/self.mass*self.dt
          self.y_vel+=net_fy/self.mass*self.dt

          self.x+=self.x_vel*self.dt
          self.y+=self.y_vel*self.dt

          self.orbit.append((self.x,self.y))

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
sun = SolarSystemBodies("Sun", YELLOW, 0,0, 1.989e30, 30)
sun.sun=True
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
          
          body.update_position(ss_bodies)
          body.draw(WINDOW)
     #print(sun.orbit)
     #print('*****************')
     #print(sun.x,sun.y)
          

     pg.display.update()
    



    
# quit pygame
pg.quit()


    