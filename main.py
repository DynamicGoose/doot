import pygame

class Enemy:
    def __init__(self, name):
        self.name = "Karl Marx"

pygame.init()

canvas = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.RESIZABLE)

pygame.display.set_caption("DOOT")
mainLoop = True

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
        if pygame.mouse.get_pressed()[2] == True:
            print("Autsch")
            pygame.display.toggle_fullscreen()
    pygame.display.update

pygame.quit()