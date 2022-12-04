import pygame
import time

map = [
    " XXXXX   ",
    " X   XXXX",
    " X   X  X",
    " XX    tX",
    "XXX XXXtX",
    "X b X XtX",
    "X bbX XXX",
    "Xa  X    ",
    "XXXXX    ",
]

map_dict = {
    " ": pygame.image.load("floor.png"),
    "X": pygame.image.load("wall.png"),
    "b": pygame.image.load("box.png"),
    "B": pygame.image.load("box_on_target.png"),
    "a": pygame.image.load("player.png"),
    "A": pygame.image.load("player_on_target.png"),
    "t": pygame.image.load("box_target.png")
}



pygame.init()    # Prepare the PyGame module for use
main_surface = pygame.display.set_mode((16*len(map[0]), 16*len(map)))


while True:

    # Look for an event from keyboard, mouse, joystick, etc.
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:   # Window close button clicked?
        break                    # Leave game loop


    # Completely redraw the surface, starting with background
    main_surface.fill((255, 255, 255))

    for i in range(len(map)):
        for j in range(len(map[i])):
            # Copy our image to the surface, at this (x,y) posn
            main_surface.blit(map_dict[map[i][j]], (j*16, i*16))

    # Now that everything is drawn, put it on display!
    pygame.display.flip()

pygame.quit()

