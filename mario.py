import pygame
import pyganim
from time import sleep
from Sprites import *

pygame.init()

W = 512
H = 464

screen = pygame.display.set_mode((W,H)) #512,480
pygame.display.set_caption('Super Mario Bros')
bg = (107,136,254)
screen.fill(bg)

clock = pygame.time.Clock()

font_path = 'Font//font.ttf'
font = pygame.font.Font(font_path,24)

main_theme = pygame.mixer.Sound('Music//main_theme.wav')
jump_effect1 = pygame.mixer.Sound('Music//jump_effect1.wav')
game_over = pygame.mixer.Sound('Music//game_over.wav')
win = pygame.mixer.Sound('Music//win.mp3')

move_speed = 5 #7
jump_power = 9.7 #10
gravity = 0.35

goomba_sprites = ['Sprites//goomba1.gif','Sprites//goomba2.gif']

mario_jump_right = ['Sprites//mariojump1.gif']
mario_jump_left = ['Sprites//mariojump2.gif']

mario_right = ['Sprites//marioright1.gif','Sprites//marioright2.gif','Sprites//marioright3.gif']
mario_left = ['Sprites//marioleft1.gif','Sprites//marioleft2.gif','Sprites//marioleft3.gif']
mario_stay = ['Sprites//mariostay.gif']

lucky = ['Sprites//lucky1.png','Sprites//lucky2.png','Sprites//lucky3.png']

bolt_anim = []
for anim in lucky:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 300))
lucky_anim = pyganim.PygAnimation(bolt_anim)
lucky_anim.play()

bolt_anim = []
for anim in goomba_sprites:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 500))
animation_goomba = pyganim.PygAnimation(bolt_anim)
animation_goomba.play()

bolt_anim = []
for anim in mario_jump_right:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 500))
anim_jump1 = pyganim.PygAnimation(bolt_anim)
anim_jump1.play()

bolt_anim = []
for anim in mario_jump_left:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 500))
anim_jump2 = pyganim.PygAnimation(bolt_anim)
anim_jump2.play()

bolt_anim = []
for anim in mario_right:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 250)) #250
anim_right = pyganim.PygAnimation(bolt_anim)
anim_right.play()

bolt_anim = []
for anim in mario_left:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 250))
anim_left = pyganim.PygAnimation(bolt_anim)
anim_left.play()

bolt_anim = []
for anim in mario_stay:
    sprite = pygame.transform.scale(pygame.image.load(anim), (32,32))
    sprite.set_colorkey(pygame.Color((107,136,254)))
    bolt_anim.append((sprite, 500))
anim_stay = pyganim.PygAnimation(bolt_anim)
anim_stay.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, plimage, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(plimage), (size_x, size_y))
        self.rect = pygame.Rect(player_x, player_y, size_x, size_y)
        self.x = player_x
        self.y = player_y
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, plimage, player_x, player_y, size_x, size_y, speedx, speedy):
        super().__init__(plimage, player_x, player_y, size_x, size_y)
        self.image.set_colorkey(pygame.Color((107,136,254)))
        self.speed_x = speedx
        self.speed_y = speedy
        self.left = False
        self.right = False
        self.up = False
        self.onGround = False
    def update(self, blocks):
        if self.left:
            self.speed_x = -move_speed
        if self.right:
            if self.rect.x >= 192:
                self.rect.x = 192
                for block in blocks:
                    block.rect.x -= self.speed_x
                for enemy in enemies:
                    enemy.rect.x -= self.speed_x
                for block in lucky_blocks:
                    block.rect.x -= self.speed_x
                    
            self.speed_x = move_speed
            
        if not (self.left or self.right):
            self.speed_x = 0
            
        if self.up:
            if self.onGround:
                jump_effect1.play()
                self.speed_y = -jump_power
                
        if not self.onGround:
            self.speed_y += gravity

        self.onGround = False

        self.rect.y += self.speed_y
        self.collide(0, self.speed_y, blocks, lucky_blocks)

        self.rect.x += self.speed_x
        self.collide(self.speed_x, 0, blocks, lucky_blocks)
        
        if self.rect.x <= 0:
            self.rect.x += 5
                    
    def collide(self, speed_x, speed_y, blocks, lucky_blocks):
        for block in blocks:
            if pygame.sprite.collide_rect(self,block):
                if speed_x > 0:
                    self.rect.right = block.rect.left
                if speed_x < 0:
                    self.rect.left = block.rect.right
                if speed_y > 0:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.speed_y = 0
                if speed_y < 0:
                    self.rect.top = block.rect.bottom
                    self.speed_y = 0
                    
        for block in lucky_blocks:
            if pygame.sprite.collide_rect(self,block):
                if speed_x > 0:
                    self.rect.right = block.rect.left
                if speed_x < 0:
                    self.rect.left = block.rect.right
                if speed_y > 0:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.speed_y = 0
                if speed_y < 0:
                    self.rect.top = block.rect.bottom
                    self.speed_y = 0
                    block0 = GameSprite('Sprites//block.png', block.rect.x, block.rect.y,32,32)
                    blocks.add(block0)
                    block.kill()

    def animate(self):
        if self.up or self.speed_y > 0.35:
            if self.speed_x < 0:
                anim_jump2.blit(screen,(self.rect.x, self.rect.y))
            else:
                anim_jump1.blit(screen,(self.rect.x, self.rect.y))
        elif animate_right:
            anim_right.blit(screen,(self.rect.x, self.rect.y))
        elif animate_left:
            anim_left.blit(screen,(self.rect.x, self.rect.y))
        elif self.speed_x == 0:
            anim_stay.blit(screen,(self.rect.x, self.rect.y))

    def check_enemy(self,enemies):
        for enemy in enemies:
            if pygame.sprite.collide_rect(self,enemy):
                if self.speed_y > 0.35:
                    enemy.animate = False
                    enemy.kill()
                else:
                    main_theme.stop()
                    game_over.play(0)
                    sleep(5)
                    player.kill()

class Goomba(GameSprite):
    def __init__(self, plimage, player_x, player_y, size_x, size_y, speedx, speedy):
        super().__init__(plimage, player_x, player_y, size_x, size_y)
        self.speed_x = speedx
        self.speed_y = speedy
        self.animate = True
        self.onGround = False
    def collide(self,group):
        for i in group:
            if pygame.sprite.collide_rect(self,i):
                if self.speed_x > 0 and self.speed_y <= 0.35:
                    self.speed_x *= -1
                elif self.speed_x < 0 and self.speed_y <= 0.35:
                    self.speed_x *= -1
                if self.speed_y > 0:
                    if self.speed_y > 0.35:
                        self.rect.bottom = i.rect.top
                    self.onGround = True
                    self.speed_y = 0
                if self.speed_y < 0:
                    self.rect.top = i.rect.bottom
                    self.speed_y = 0
        
    def update(self):
        if not self.onGround:
            self.speed_y += gravity

        self.onGround = False

        self.rect.y += self.speed_y
        self.collide(blocks)
        self.collide(lucky_blocks)

        self.rect.x += self.speed_x
        self.collide(blocks)
        self.collide(lucky_blocks)

enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
lucky_blocks = pygame.sprite.Group()

#####################

#first ground
for i in range(0,2177,32):
    block = GameSprite('Sprites//ground_block.png',i,448,32,32)
    block1 = GameSprite('Sprites//ground_block.png',i,416,32,32)
    blocks.add(block)
    blocks.add(block1)

#objects on first ground

lucky_block = GameSprite('Sprites//lucky_block.png',512,288,32,32)
lucky_blocks.add(lucky_block)

#goomba
goomba1 = Goomba('Sprites//dead_goomba.gif',640,384,32,32,-2,0)
enemies.add(goomba1)

#5 blocks(2 lucky blocks)
count = 0
for i in range(640,800,32):
    if count == 1 or count == 3:
        block = GameSprite('Sprites//lucky_block.png',i,288,32,32)
        lucky_blocks.add(block)
    else:
        block = GameSprite('Sprites//brick_block4.png',i,288,32,32)
        blocks.add(block)
    count += 1

block = GameSprite('Sprites//lucky_block.png',704,160,32,32)
lucky_blocks.add(block)

#first pipe
pipe1 = GameSprite('Sprites//pipe2.png',896,352,64,64)
blocks.add(pipe1)
    
#second pipe
pipe2 = GameSprite('Sprites//pipe3.png',1216,320,64,96)
blocks.add(pipe2)

#goomba
goomba2 = Goomba('Sprites//dead_goomba.gif',1300,384,32,32,-2,0)
enemies.add(goomba2)

#thirst pipe
pipe3 = GameSprite('Sprites//pipe3.png',1472,288,64,128)
blocks.add(pipe3)

goomba = Goomba('Sprites//dead_goomba.gif',1550,384,32,32,-2,0)
goomba1 = Goomba('Sprites//dead_goomba.gif',1600,384,32,32,-2,0)
enemies.add(goomba)
enemies.add(goomba1)

#four pipe
pipe4 = GameSprite('Sprites//pipe3.png',1824,288,64,128)
blocks.add(pipe4)

##########################

#second ground
for i in range(2272,2688,32):
    block = GameSprite('Sprites//ground_block.png',i,448,32,32)
    block1 = GameSprite('Sprites//ground_block.png',i,416,32,32)
    blocks.add(block)
    blocks.add(block1)

#objects on second ground

#three blocks(1 lucky block)
count = 0
for i in range(2464,2529,32):
    if count == 1:
        block = GameSprite('Sprites//lucky_block.png',i,288,32,32)
        lucky_blocks.add(block)
    else:
        block = GameSprite('Sprites//brick_block4.png',i,288,32,32)
        blocks.add(block)
    count += 1

goomba1 = Goomba('Sprites//dead_goomba.gif',2528,256,32,32,-2,0)
goomba2 = Goomba('Sprites//dead_goomba.gif',2600,128,32,32,-2,0)
enemies.add(goomba1)
enemies.add(goomba2)

#8 blocks
for i in range(2560,2721,32):
    block = GameSprite('Sprites//brick_block4.png',i,160,32,32)
    blocks.add(block)

############################

#thirst ground
for i in range(2784,4801,32):
    block = GameSprite('Sprites//ground_block.png',i,448,32,32)
    block1 = GameSprite('Sprites//ground_block.png',i,416,32,32)
    blocks.add(block)
    blocks.add(block1)

#objects on thirst ground

#4 blocks(1 lucky block)
count = 0
for i in range(2848,2945,32):
    if count == 3:
        block = GameSprite('Sprites//lucky_block.png',i,160,32,32)
        lucky_blocks.add(block)
    else:
        block = GameSprite('Sprites//brick_block4.png',i,160,32,32)
        blocks.add(block)
    count += 1

block = GameSprite('Sprites//brick_block4.png',2944,288,32,32)
blocks.add(block)

goomba = Goomba('Sprites//dead_goomba.gif',3000,384,32,32,-2,0)
goomba1 = Goomba('Sprites//dead_goomba.gif',3036,384,32,32,-2,0)
enemies.add(goomba)
enemies.add(goomba1)

for i in range(3136,3169,32):
    block = GameSprite('Sprites//brick_block4.png',i,288,32,32)
    blocks.add(block)

lucky_block = GameSprite('Sprites//lucky_block.png',3328,288,32,32)
lucky_blocks.add(lucky_block)
lucky_block = GameSprite('Sprites//lucky_block.png',3424,288,32,32)
lucky_blocks.add(lucky_block)
lucky_block = GameSprite('Sprites//lucky_block.png',3520,288,32,32)
lucky_blocks.add(lucky_block)
lucky_block = GameSprite('Sprites//lucky_block.png',3424,160,32,32)
lucky_blocks.add(lucky_block)

goomba = Goomba('Sprites//dead_goomba.gif',3530,384,32,32,-2,0)
goomba1 = Goomba('Sprites//dead_goomba.gif',3570,384,32,32,-2,0)
enemies.add(goomba)
enemies.add(goomba1)

brick_block = GameSprite('Sprites//brick_block4.png',3712,288,32,32)
blocks.add(brick_block)

for i in range(3808,3904,32):
    brick_block = GameSprite('Sprites//brick_block4.png',i,160,32,32)
    blocks.add(brick_block)

goomba = Goomba('Sprites//dead_goomba.gif',3905,384,32,32,-2,0)
goomba1 = Goomba('Sprites//dead_goomba.gif',3938,384,32,32,-2,0)
enemies.add(goomba)
enemies.add(goomba1)
    
count = 0
for i in range(4031,4128,32):
    if count == 1 or count == 2:
        block = GameSprite('Sprites//lucky_block.png',i,160,32,32)
        lucky_blocks.add(block)
    else:
        block = GameSprite('Sprites//brick_block4.png',i,160,32,32)
        blocks.add(block)
    count += 1

goomba = Goomba('Sprites//dead_goomba.gif',4062,384,32,32,-2,0)
goomba1 = Goomba('Sprites//dead_goomba.gif',4096,384,32,32,-2,0)
enemies.add(goomba)
enemies.add(goomba1)

for i in range(4063,4096,32):
    block = GameSprite('Sprites//brick_block4.png',i,288,32,32)
    blocks.add(block)

for i in range(4224,4321,32):
    block = GameSprite('Sprites//block.png',i,384,32,32)
    blocks.add(block)
for i in range(4256,4321,32):
    block = GameSprite('Sprites//block.png',i,352,32,32)
    blocks.add(block)
for i in range(4288,4321,32):
    block = GameSprite('Sprites//block.png',i,320,32,32)
    blocks.add(block)
block = GameSprite('Sprites//block.png',4320,288,32,32)
blocks.add(block)



block = GameSprite('Sprites//block.png',4416,288,32,32)
blocks.add(block)
for i in range(4416,4449,32):
    block = GameSprite('Sprites//block.png',i,320,32,32)
    blocks.add(block)
for i in range(4416,4481,32):
    block = GameSprite('Sprites//block.png',i,352,32,32)
    blocks.add(block)
for i in range(4416,4513,32):
    block = GameSprite('Sprites//block.png',i,384,32,32)
    blocks.add(block)

    

for i in range(4672,4801,32):
    block = GameSprite('Sprites//block.png',i,384,32,32)
    blocks.add(block)
for i in range(4704,4801,32):
    block = GameSprite('Sprites//block.png',i,352,32,32)
    blocks.add(block)
for i in range(4736,4801,32):
    block = GameSprite('Sprites//block.png',i,320,32,32)
    blocks.add(block)
for i in range(4768,4801,32):
    block = GameSprite('Sprites//block.png',i,288,32,32)
    blocks.add(block)


#four ground
for i in range(4896,7000,32):
    block = GameSprite('Sprites//ground_block.png',i,448,32,32)
    block1 = GameSprite('Sprites//ground_block.png',i,416,32,32)
    blocks.add(block)
    blocks.add(block1)


block = GameSprite('Sprites//block.png',4896,288,32,32)
blocks.add(block)
for i in range(4896,4929,32):
    block = GameSprite('Sprites//block.png',i,320,32,32)
    blocks.add(block)
for i in range(4896,4961,32):
    block = GameSprite('Sprites//block.png',i,352,32,32)
    blocks.add(block)
for i in range(4896,4993,32):
    block = GameSprite('Sprites//block.png',i,384,32,32)
    blocks.add(block)

pipe = GameSprite('Sprites//pipe2.png',5152,352,64,64)
blocks.add(pipe)

goomba = Goomba('Sprites//dead_goomba.gif',5220,384,32,32,-2,0)
goomba1 = Goomba('Sprites//dead_goomba.gif',5260,384,32,32,-2,0)
enemies.add(goomba)
enemies.add(goomba1)

count = 0
for i in range(5312,5409,32):
    if count == 2:
        block = GameSprite('Sprites//lucky_block.png',i,288,32,32)
        lucky_blocks.add(block)
    else:
        block = GameSprite('Sprites//brick_block4.png',i,288,32,32)
        blocks.add(block)
    count += 1

pipe2 = GameSprite('Sprites//pipe2.png',5664,352,64,64)
blocks.add(pipe2)

for i in range(5728,6016,32):
    block = GameSprite('Sprites//block.png',i,384,32,32)
    blocks.add(block)
for i in range(5760,6016,32):
    block = GameSprite('Sprites//block.png',i,352,32,32)
    blocks.add(block)
for i in range(5792,6016,32):
    block = GameSprite('Sprites//block.png',i,320,32,32)
    blocks.add(block)
for i in range(5824,6016,32):
    block = GameSprite('Sprites//block.png',i,288,32,32)
    blocks.add(block)
for i in range(5856,6016,32):
    block = GameSprite('Sprites//block.png',i,256,32,32)
    blocks.add(block)
for i in range(5888,6016,32):
    block = GameSprite('Sprites//block.png',i,224,32,32)
    blocks.add(block)
for i in range(5920,6016,32):
    block = GameSprite('Sprites//block.png',i,192,32,32)
    blocks.add(block)
for i in range(5952,6016,32):
    block = GameSprite('Sprites//block.png',i,160,32,32)
    blocks.add(block)

flag_block = GameSprite('Sprites//block.png',6272,384,32,32)
blocks.add(flag_block)
flag = GameSprite('Sprites//flag.png',6235,64,64,320)
blocks.add(flag)

#################################

player = Player('Sprites//mariostay.gif',80,384,32,32,0,0) #32,43
player_check = pygame.sprite.Group()
player_check.add(player)

run = True
sound_of_jump = True
animate_right = False
animate_left = False
animate_jump = False
#fall = False

start_text = 'press W to start'
instruction = 'w,a,s,d - movement'
text = font.render(str(start_text), True, (255,255,255))
ins = font.render(str(instruction), True, (255,255,255))

start_menu = True
start_menu_blocks = pygame.sprite.Group()
for i in range(0,513,32):
    block = GameSprite('Sprites//ground_block.png',i,448,32,32)
    block1 = GameSprite('Sprites//ground_block.png',i,416,32,32)
    start_menu_blocks.add(block)
    start_menu_blocks.add(block1)

while start_menu:
    screen.fill(bg)
    for block in start_menu_blocks:
        block.reset()
        
    screen.blit(text, (110, H//2))
    screen.blit(ins, (110, 154))
    
    player.reset()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            start_menu = False
        if event.type == pygame.QUIT:
            start_menu = False
            run = False

    pygame.display.update()
    clock.tick(50)

main_theme.play(-1)

score = 0
length_goomba = len(enemies)

coins = 0
length_lucky = len(lucky_blocks)

timer = 400
while run:
    time = font.render(str(timer), True, (255,255,255))
    time_text = font.render(str('TIME'), True, (255,255,255))
        
    coin_count = font.render(str(coins), True, (255,255,255))
    coin_text = font.render(str('COINS'), True, (255,255,255))
    
    score_text = font.render(str(score), True, (255,255,255))
    player_name = font.render(str('MARIO'), True, (255,255,255))

    world = font.render(str('WORLD'), True, (255,255,255))
    world1 = font.render(str('1-1'), True, (255,255,255))
    
    score += (length_goomba - len(enemies))* 100
    length_goomba = len(enemies)
    coins += (length_lucky - len(lucky_blocks))
    length_lucky = len(lucky_blocks)

    if player.rect.x + 32 == flag.rect.x: #or player.rect.bottom == flag.rect.top:
        main_theme.stop()
        win.play(0)
        sleep(8)
        run = False
        
    screen.fill(bg)

    if player.rect.y > 510:
        player.kill()
        main_theme.stop()
        game_over.play(0)
        sleep(5)
        
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.right = True
                animate_right = True
            if event.key == pygame.K_a:
                player.left = True
                animate_left = True
            if event.key == pygame.K_w:
                player.up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.right = False
                animate_right = False
            if event.key == pygame.K_a:
                player.left = False
                animate_left = False
            if event.key == pygame.K_w:
                player.speed_y = 0 
                player.up = False
        if event.type == pygame.QUIT:
                run = False
  
    player.update(blocks)
    
    for block in blocks:
        if block.rect.x <= -200:
            block.kill()
        if block.rect.x > -45 and block.rect.x < 550:
            block.reset()
    
    for enemy in enemies:
        if enemy.rect.x <= -50:
            enemy.kill()
            length_goomba = len(enemies)
        if enemy.rect.y >= 416:
            enemy.speed_x = 0
        if enemy.rect.x > -45 and enemy.rect.x < 500:
            enemy.collide(blocks)
            #enemy.collide(enemies)
            enemy.update()
            
        if enemy.animate:     
            animation_goomba.blit(screen,(enemy.rect.x, enemy.rect.y))
        else:
            enemy.speed_x = 0
            enemy.speed_y = 0
            enemy.reset()

    for block in lucky_blocks:
        if block.rect.x <= -200:
            block.kill()
            length_lucky = len(lucky_blocks)
        if block.rect.x > -45 and block.rect.x < 550:
            lucky_anim.blit(screen,(block.rect.x, block.rect.y))

    player.animate()
    player.check_enemy(enemies)
    
    screen.blit(player_name, (25, 0))
    screen.blit(score_text, (25, 25))

    screen.blit(coin_text, (150, 0))
    screen.blit(coin_count, (150, 25))

    screen.blit(world, (275, 0))
    screen.blit(world1, (300, 25))

    #screen.blit(time, (400, 25))
    #screen.blit(time_text, (400, 0))
    #timer -= 1
    
    if len(player_check) == 0:
        break

    pygame.display.update()
    clock.tick(50)
pygame.quit()
