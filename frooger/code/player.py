import pygame
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.import_assets()
        self.frame_index = 0
        self.status = 'down'
        #self.image = self.animation[0]
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

        


    def import_assets(self):
        #path = 'graphics/player/right/'
        #self.animation = [pygame.image.load(f'{path}{frame}.png').convert_alpha() for frame in range(4)]    

        self.animations = {}
        for index, folder in enumerate(walk('graphics/player')):
            #print(folder)
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    #print(folder[0])
                    path = folder[0].replace("\\","/") + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)
                    #print(key)
                    self.animations[key].append(surf)
        #print(self.animations)

            
        
    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def input(self):

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def animate(self, dt):
        current_animations = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt
            self.image = current_animations[int(self.frame_index) % 4]
        else:
            self.frame_index = 0
        self.image = current_animations[int(self.frame_index) %4]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        



