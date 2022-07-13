from random import randint, uniform
import pygame, sys


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.mask = pygame.mask.from_surface(self.image)

        self.can_shoot = True
        self.shoot_time = None

        
        self.laser_sound = pygame.mixer.Sound('sounds/laser.ogg')
        

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    
    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
    
    def laser_shoot(self):
        if self.can_shoot and pygame.mouse.get_pressed()[0]:
                #print(f'shoot {randint(1,10)}')
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()

                Laser(self.rect.midtop, laser_groups)
                self.laser_sound.play()
    
    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_groups, False,pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()
        self.meteor_collision()

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = position)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_groups, True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
    
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.meteor_collision()
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos,  groups):
        super().__init__(groups)
        meteor_surf = pygame.image.load('graphics/meteor.png').convert_alpha()
        metor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.7)
        self.scaled_surf = pygame.transform.scale(meteor_surf, metor_size) 
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5), 1)
        self.speed = randint(400, 600)

        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

class Score:
    def __init__(self):
        self.font = pygame.font.Font('graphics/subatomic.ttf', 50)
        
    
    def display(self):
        score_text = f'Score: {pygame.time.get_ticks()//1000}'
        text_surf = self.font.render(score_text, True, (255, 255, 255))   
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(text_surf, text_rect)





pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()


#bacground
background_surface = pygame.image.load('graphics/background.png').convert()

# groups
spaceship_group = pygame.sprite.GroupSingle()
laser_groups = pygame.sprite.Group()
meteor_groups = pygame.sprite.Group()

ship = Ship(spaceship_group)
score = Score()


meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

bg_music = pygame.mixer.Sound('sounds/music.wav')
bg_music.set_volume(0.1)
bg_music.play(-1)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteor_y_pos = randint(-150, 50)
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Meteor((meteor_x_pos, meteor_y_pos), meteor_groups)

    dt = clock.tick(120) / 1000
    #print(clock.get_fps())
    
    # background
    display_surface.blit(background_surface, (0,0))
    

    #update
    spaceship_group.update()
    laser_groups.update()
    meteor_groups.update()
   

    score.display()

    #graphics
    spaceship_group.draw(display_surface)
    laser_groups.draw(display_surface)
    meteor_groups.draw(display_surface)
    
    

    pygame.display.update()
