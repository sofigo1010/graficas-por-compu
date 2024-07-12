import pygame
from pygame.locals import *
from gl import Renderer

width = 960
height = 540

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rend = Renderer(screen) 

pl1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
pl2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
pl3 = [(377, 249), (411, 197), (436, 249)]
pl4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
pl5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

isRunning = True

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()
    
    rend.poligono(pl1, (1, 1, 0))   
    rend.poligono(pl2, (0.5, 0, 0.5))  
    rend.poligono(pl3, (0, 1, 1))   
    rend.poligono(pl4, (1, 1, 1))   
    rend.poligono(pl5, (0, 0, 0))  
    
    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFramebuffer("output.bmp")
pygame.quit()
