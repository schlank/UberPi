import pygame
from pygame.locals import *

pygame.init()

pygame.key.set_repeat(100, 100)

while 1:
    if pygame.key.get_pressed[K_t]:
            print("go forward")
                
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            
            if event.type == pygame.K_s:
                print("go backward")
        if event.type == pygame.KEYUP:
            print("stop")
