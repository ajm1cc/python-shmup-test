import pygame
import sys

pygame.init()
size = (400, 300)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pygame Test")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
