import pygame


class Keyboard(object):

    events = pygame.event.get()
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                print("UP")
                moveUp = True
            elif event.key == pygame.K_DOWN:
                moveDown = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_ESCAPE:
                moveQuit = True
            elif event.key == pygame.K_1:
                say = "Hello. Human.  May I please have assistance."
            elif event.key == pygame.K_2:
                say = "Floor 11 please.  I have a delivery to make.  Time.  Is Money."
            elif event.key == pygame.K_3:
                say = "Floor 10 please."
            elif event.key == pygame.K_4:
                say = "Thank You.  Human. You will be spared in the coming war.  Have a good day."
            elif event.key == pygame.K_5:
                say = "How is your day going? Human.  Nice weather we are having."
            elif event.key == pygame.K_6:
                say = "oh. Good.  That is nice."
            elif event.key == pygame.K_7:
                say = "Mellisa.  Down here. Mellisa.  I have a delivery for you."
            elif event.key == pygame.K_8:
                say = "The number 8. is for Sophia to add her words.  Most likely ending up in poop words."
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                print("UP KEYUP")
                moveUp = False
            elif event.key == pygame.K_DOWN:
                moveDown = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_ESCAPE:
                moveQuit = False
