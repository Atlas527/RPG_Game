import pygame
import os

pygame.init()

#screen
screen_width = 800
screen_height = int(screen_width * 0.8)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('RPG Game')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75



#define player action variables
moving_left = False
moving_right = False
shoot = False

# load images
#bullet
bullet_img = pygame.image.load('img/player/png/Bullets/0.png.png').convert_alpha()

#define colors
BG = (144, 201, 120)
RED = (255,0,0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 600), (screen_width, 600))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite. __init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load all images for players
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f"img/{self.char_type}/png/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/png/{animation}/{i}.png.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #reset movement variable
        dx = 0
        dy = 0


        #assigned movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.in_air = False


        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy


    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation has run out then reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different than the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            update_time = pygame.time.get_ticks()



    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip,False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill

#create sprite groups
bullet_group = pygame.sprite.Group()



player = Soldier("player",200,200,1, 5)
enemy = Soldier("enemy", 400, 200, 1, 5)

#event handler
run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.update_animation()
    player.draw()
    enemy.draw()

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    #update to player actions
    if player.alive:
        #shoot bullets
        if shoot:
            bullet = Bullet(player.rect.centerx + (0.6 * player.rect.size[0] * player.direction), player.rect.centery, player.direction)
            bullet_group.add(bullet)
        if player.in_air:
            player.update_action(2)#2: jump
        elif moving_left or moving_right:
            player.update_action(1)#1 means run
        else:
            player.update_action(0)
    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True



        #keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False


    pygame.display.update()


pygame.QUIT()