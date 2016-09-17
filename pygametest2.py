import pygame
import os
pygame.init()

# make sure pygame doesn't try to open an output window
os.environ["SDL_VIDEODRIVER"] = "dummy"

DEBUG = False
HOST = "localhost"
PORT = "50000"
WHEEL = "G27 Racing Wheel"

try:

  wheel = None
  for j in range(0,pygame.joystick.get_count()):
    if pygame.joystick.Joystick(j).get_name() == WHEEL:
      wheel = pygame.joystick.Joystick(j)
      wheel.init()
      print "Found", wheel.get_name()

  if not wheel:
    print "No G27 steering wheel found"
    exit(-1)
except Exception as e:
  print e

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("hey you pressed 0")
            if event.key == pygame.K_1:
                print("DOing whatever")
        else:
            print("Event Type: %s", event.type)
            print("Event :", event)
