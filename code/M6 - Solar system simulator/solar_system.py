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
WINDOW = pg.display.set_mode((WIDTH-150,HEIGHT-150))
pg.display.set_caption('Solar System Simulator')


#define colors for simulation
WHITE = (255,255,255)

#create simulation
run = True

while run:
    WINDOW.fill(WHITE)

    for event in pg.event.get():
        print(event)
        if event.type == pg.QUIT:
            run = False

    pg.display.update()
        
# quit pygame
pg.quit()


    