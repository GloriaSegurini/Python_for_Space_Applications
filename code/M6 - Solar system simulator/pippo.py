# Libraries
import pygame as pg
import math
from random import randint

# Initialize Pygame
pg.init()

# Create window 
screen_info = pg.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
WINDOW = pg.display.set_mode((WIDTH-150,HEIGHT-150)) ############### pygame window
pg.display.set_caption('Solar System Simulator') ############ solar system simulator



#define colors for simulation
#WHITE = (255,255,255)
YELLOW = (255,255,0)
GRAY = (128,128,128)


# Class Solar System Bodies
class SolarSystemBodies:
     
     #astronomical unit = distance from Sun to Earth
     AU = 1.496e11
     SCALE = 100/AU
     
     def __init__(self, name, color, x,y, mass, radius):
          self.name = name
          self.color = color
          self.x = x
          self.y = y
          self.mass = mass
          self.radius = radius
    
    # Method 1: draw bodies on the simulator
     def draw_body(self, WINDOW):
        x = self.x*SolarSystemBodies.SCALE + WIDTH//2
        y = self.y*SolarSystemBodies.SCALE + WIDTH//2
        pg.draw.circle(surface = WINDOW, color = self.color, center=(x,y), radius = self.radius )

# Stars list with color, center and radius
star_list = [{'color': (randint(190,255), randint(190,255), randint(190,255)),
               'center':(randint(5, WIDTH-155), randint(5, WIDTH-155)),
               'radius': (randint(1,2))
               }
            for star in range(100)]


# Function to draw stars in teh background
def draw_stars(stars_list, radius):
     for star in stars_list:
          pg.draw.circle(WINDOW, star['color'], star['center'], radius)




#create simulation
run = True

while run:
    radius = randint(1,3)
    for i in range(1000000):
     print('here')

     for event in pg.event.get():
            
            if event.type == pg.QUIT:
                run = False
                
    draw_stars(star_list, radius)
    
             
    pg.display.update()
    

   
# quit pygame
pg.quit()


    
