import pygame, sys
import settings
from player import Player
from car import Car

pygame.init()
display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
pygame.display.set_caption('Frooger')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player((600,500), all_sprites)
car = Car((700,200), all_sprites)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    dt = clock.tick() / 1000

    display_surface.fill('black')

    all_sprites.update(dt)


    all_sprites.draw(display_surface)
   

    pygame.display.update()