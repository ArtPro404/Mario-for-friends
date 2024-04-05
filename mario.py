import pygame
from time import sleep

pygame.init()

screen = pygame.display.set_mode((512,464)) #512,480
pygame.display.set_caption('Super Mario Bros')
bg = (107,136,254)
screen.fill(bg)

clock = pygame.time.Clock()

main_theme = pygame.mixer.Sound('main_theme.wav')
jump_effect1 = pygame.mixer.Sound('jump_effect1.wav')
game_over = pygame.mixer.Sound('game_over.wav')

move_speed = 7
jump_power = 10
gravity = 0.35

class GameSprite(pygame.sprite.Sprite): #pygame.sprite.Sprite
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
                    block.rect.x -= 4
                for enemy in enemies:
                    enemy.rect.x -= 4
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
        self.collide(0, self.speed_y, blocks)

        self.rect.x += self.speed_x
        self.collide(self.speed_x, 0,blocks)
        
        if self.rect.x <= 0:
            self.rect.x += 4
    def collide(self, speed_x, speed_y, blocks):
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

class Enemy(GameSprite):
    def __init__(self, plimage, player_x, player_y, size_x, size_y, speedx, speedy):
        super().__init__(plimage, player_x, player_y, size_x, size_y)
        self.speed_x = speedx
        self.speed_y = speedy
    def swap_side(self):
        for block in blocks:
            if pygame.sprite.collide_rect(self,block):
                if self.speed_x > 0:
                    #self.rect.right = block.rect.left
                    self.speed_x *= -1
                elif self.speed_x < 0:
                    #self.rect.left = block.rect.right
                    self.speed_x *= -1
                if self.speed_y > 0:
                    self.rect.bottom = block.rect.top
                    self.speed_y = 0
                if self.speed_y < 0:
                    self.rect.top = block.rect.bottom
                    self.speed_y = 0
                    
            #if not self.onGround:
                #self.speed_y += gravity
                
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()

#ground
#for i in range(0,2177,32):
    #block = GameSprite('ground_block.png',i,448,32,32)
    #block1 = GameSprite('ground_block.png',i,416,32,32)
    #blocks.add(block)
    #blocks.add(block1)
    
for i in range(0,513,32):
    block = GameSprite('ground_block.png',i,448,32,32)
    block1 = GameSprite('ground_block.png',i,416,32,32)
    blocks.add(block)
    blocks.add(block1)
    
#for i in range(2272,2721,32):
    #block = GameSprite('ground_block.png',i,448,32,32)
    #block1 = GameSprite('ground_block.png',i,416,32,32)
    #blocks.add(block)
    #blocks.add(block1)

#for i in range(2848,3500,32):
    #block = GameSprite('ground_block.png',i,448,32,32)
    #block1 = GameSprite('ground_block.png',i,416,32,32)
    #blocks.add(block)
    #blocks.add(block1)
    
lucky_block = GameSprite('lucky_block.png',512,288,32,32)
blocks.add(lucky_block)

#5 blocks(2 lucky blocks)
count = 0
for i in range(640,800,32):
    if count == 1 or count == 3:
        block = GameSprite('lucky_block.png',i,288,32,32)
    else:
        block = GameSprite('ground_block.png',i,288,32,32)
    blocks.add(block)
    count += 1

block = GameSprite('lucky_block.png',704,160,32,32)
blocks.add(block)

#first pipe
for i in range(896,929,32): # 928
    block = GameSprite('ground_block.png',i,384,32,32)
    block1 = GameSprite('ground_block.png',i,352,32,32)
    blocks.add(block)
    blocks.add(block1)
    
#second pipe
for i in range(1216,1249,32):
    block = GameSprite('ground_block.png',i,384,32,32)
    block1 = GameSprite('ground_block.png',i,352,32,32)
    block2 = GameSprite('ground_block.png',i,320,32,32)
    blocks.add(block)
    blocks.add(block1)
    blocks.add(block2)

#first goomba
goomba = Enemy('mario.png',1300,384,32,32,-2,0)
enemies.add(goomba)

#thirst pipe
for i in range(1472,1505,32):
    block = GameSprite('ground_block.png',i,384,32,32)
    block1 = GameSprite('ground_block.png',i,352,32,32)
    block2 = GameSprite('ground_block.png',i,320,32,32)
    block3 = GameSprite('ground_block.png',i,288,32,32)
    blocks.add(block)
    blocks.add(block1)
    blocks.add(block2)
    blocks.add(block3)

#four pipe
for i in range(1824,1857,32):
    block = GameSprite('ground_block.png',i,384,32,32)
    block1 = GameSprite('ground_block.png',i,352,32,32)
    block2 = GameSprite('ground_block.png',i,320,32,32)
    block3 = GameSprite('ground_block.png',i,288,32,32)
    blocks.add(block)
    blocks.add(block1)
    blocks.add(block2)
    blocks.add(block3)

player = Player('mario1.png',80,373,32,32,0,0) #32,43

run = True
sound_of_jump = True
# sprint = False

main_theme.play(-1)

while run:

    #game_over
    
    #fall
    if player.rect.y > 510:
        player.rect.y = 373
        player.rect.x = -40
        
        main_theme.stop()
        game_over.play(0)
        sleep(5)
        run = False
        
    screen.fill(bg)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.right = True
            if event.key == pygame.K_a:
                player.left = True
            if event.key == pygame.K_w:
                player.up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.right = False
            if event.key == pygame.K_a:
                player.left = False
            if event.key == pygame.K_w:
                #player.speed_y += gravity
                player.up = False
        if event.type == pygame.QUIT:
                run = False
  
    player.update(blocks)
    player.reset()
    
    for block in blocks:
        if block.rect.x <= -32 and (block.rect.y == 448 or block.rect.y == 416):
            block.rect.x = 512
        if block.rect.x <= -50:
            block.kill()
        if block.rect.x > -45 and block.rect.x < 550:
            block.reset()
            
    #if blocks.sprites()[-1].rect.x < 432:
        #new_block = GameSprite('ground_block.png',512,448,32,32)
        #new_block1 = GameSprite('ground_block.png',512,416,32,32)
        #blocks.add(new_block)
        #blocks.add(new_block1)

    
    for enemy in enemies:
        if enemy.rect.x <= -50:
            enemy.kill()
        if enemy.rect.x > -45 and enemy.rect.x < 550:
            enemy.update()
            enemy.swap_side()
            enemy.reset()
    
    pygame.display.update()
    clock.tick(50)
pygame.quit()
