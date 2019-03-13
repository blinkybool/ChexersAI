#!/usr/bin/env python
#
#
#
#
#

# documentation string of this module
"""
Chexers.
"""
# some informational variables
__author__    = "$Author: Billy $"

#----------------------------- actual code --------------------------------

# import the pygame module, so you can use it
import pygame as pg
from hexboard import HexBoard

SCREEN_W = 1024
SCREEN_H = 1024

CENTRE_X = SCREEN_W/2
CENTRE_Y = SCREEN_H/2

# define a main function
def main():
    
    # initialize the pygame module
    pg.init()
    
    # load and set the logo
    logo = pg.image.load("logo32x32.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("chexers")
    
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode((SCREEN_W,SCREEN_H))

    hexagon = pg.transform.scale(pg.image.load("hexagon.png"), (100,100))
    
    
    screen.fill((255,255,255))
    screen.blit(hexagon, (CENTRE_X+50,CENTRE_Y))
    screen.blit(hexagon, (CENTRE_X-50,CENTRE_Y))
    pg.display.flip()
    
    
    # define a variable to control the main loop
    running = True
    
    # main loop
    while running:
        
        # event handling, gets all event from the eventqueue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()