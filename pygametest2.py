import pygame
pygame.init()
pygame.display.set_mode
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("hey you pressed 0")
            if event.key == pygame.K_1:
                print("DOing whatever")
