import pygame
import sys
import random

from pygame.constants import K_SPACE, K_UP

pygame.init()

# set title and image for window 
pygame.display.set_caption("Chrome Dino Game")
dino_icon = pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\dino.jpg')
pygame.display.set_icon(dino_icon)

# images for the background and environment
game_screen = pygame.display.set_mode((1100, 800)) # creates display
ground = pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Other\\Track.png')
cloud = pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Other\\Cloud.png').convert_alpha()

# images for the player's actions
playerRun = [pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Dino\DinoRun1.png'),
             pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Dino\DinoRun2.png')]

playerDuck = [pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Dino\DinoDuck1.png'),
              pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Dino\DinoDuck2.png')]

playerJump = pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Dino\DinoJump.png')

# images for the obstacles
smallCacti = [pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Cactus\\SmallCactus1.png'),
         pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Cactus\\SmallCactus2.png'),
         pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Cactus\\SmallCactus3.png')]

bigCacti = [pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Cactus\\LargeCactus1.png'),
         pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Cactus\\LargeCactus2.png'),
         pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Cactus\\LargeCactus3.png')]

birds = [pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Bird\\Bird1.png'),
        pygame.image.load('C:\\Users\\Owner\\Documents\\GitHub\\Python Projects\\pygame-ChromeDinoRun\\Assets\\Bird\\Bird2.png')]
         
birds[0] = pygame.transform.scale(birds[0], (birds[0].get_width() - 20, birds[0].get_height() - 20))
birds[1] = pygame.transform.scale(birds[1], (birds[1].get_width() - 20, birds[1].get_height() - 20))


# used for fps
clock = pygame.time.Clock()

# class for Dinosaur object
class Dino:
    runIndex = 0
    duckIndex = 0

    jumpState = False
    runState = True
    duckState = False

    dinoJumpVel = 9
    dinoY = 300

    dino_rect = playerRun[0].get_rect(topleft = (80, 300))

    def _init_(self):
        # define variables for current state
        self.jumpState = False
        self.runState = True
        self.duckState = False

    def run(self):
        game_screen.blit(playerRun[self.runIndex], (80, 300))

        self.runIndex += 1
        if (self.runIndex >= len(playerRun)):
            self.runIndex = 0
        self.dino_rect = playerRun[self.runIndex].get_rect(topleft = (80, 300)) # update the rectangle representing dino with latest image  
    
    def duck(self):
        game_screen.blit(playerDuck[self.duckIndex], (80, 340))

        self.duckIndex += 1
        if (self.duckIndex >= len(playerDuck)):
            self.duckIndex = 0
        
        self.dino_rect = playerDuck[self.duckIndex].get_rect(topleft = (80, 340))
    
    def jump(self):
        game_screen.blit(playerJump, (80, self.dinoY))

        if self.jumpState:
            self.dinoY -= self.dinoJumpVel * 4
            self.dinoJumpVel -= 0.8

        if self.dinoJumpVel < -9:
            self.jumpState = False
            self.dinoJumpVel = 9
            self.dinoY = 300
        
        self.dino_rect = playerJump.get_rect(topleft = (80, self.dinoY))

# class for Clouds that will pass across background    
class Cloud:
    def __init__(self):
        # x1 and x2 represent two different clouds
        self.x1 = 1100 + random.randint(800, 1000) # 1100px is the length of the screen + a random spot while scrolling
        self.y1 = random.randint(100, 150)

        self.x2 = 1100 + random.randint(200, 400)
        self.y2 = random.randint(50, 100)

    def cloudDraw(self): # uses random to place it randomly across screen
        self.x1 -= groundSpeed
        self.x2 -= groundSpeed
        
        game_screen.blit(cloud, (self.x1, self.y1))
        game_screen.blit(cloud, (self.x2, self.y2))

        # once entire cloud passes left of screen reset its position
        if self.x1 < -cloud.get_width():
            self.x1 = 1100 + random.randint(800, 1000)
            self.y1 = random.randint(100, 150)
        
        if self.x2 < -cloud.get_width():
            self.x2 = 1100 + random.randint(200, 400)
            self.y2 = random.randint(50, 100)

# class for track 
groundSpeed = 10
class Ground:
    def __init__(self):
        # obtain start and end points of image to use for scrolling
        self.x1 = 0
        self.x2 = ground.get_width()
    
    def scroll(self):
        self.x1 -= groundSpeed
        self.x2 -= groundSpeed

        if self.x1 + ground.get_width() < 0:
            self.x1 = self.x2 + ground.get_width()
        
        if self.x2 + ground.get_width() < 0:
            self.x2 = self.x1 + ground.get_width()

        game_screen.blit(ground, (self.x1, 360))
        game_screen.blit(ground, (self.x2, 360))

class Cacti():
    small_rect = None
    big_rect = None 

    def __init__(self):
        self.x1 = random.randint(500, 700)
        self.y1 = 310
        self.image1 = random.choice(smallCacti)

        self.x2 = random.randint(1000, 1100)
        self.y2 = 285
        self.image2 = random.choice(bigCacti)

    def obstacleDraw(self):
        self.small_rect = self.image1.get_rect(topleft = (self.x1, self.y1))
        self.big_rect = self.image2.get_rect(topleft = (self.x2, self.y2))

        # update rectangles to make hitbox smaller during collision
        self.small_rect = self.small_rect.inflate(-20, -15)
        self.big_rect = self.big_rect.inflate(-10, -85)

        self.x1 -= groundSpeed
        self.x2 -= groundSpeed

        game_screen.blit(self.image1, (self.x1, self.y1))
        game_screen.blit(self.image2, (self.x2, self.y2))

        if self.x1 < -self.image1.get_width():
            self.image1 = random.choice(smallCacti)
            self.x1 = 600 + random.randint(500, 800)

        if self.x2 < -self.image2.get_width():
            self.image2 = random.choice(bigCacti)
            self.x2 = 600 + random.randint(800, 1000)

class Bird():
    bird_rect = None
    flyIndex = 0
    pause = 0

    def __init__(self):
        # initialize starting position of the newest bird on screen
        self.x = 1200
        self.y = random.randint(50, 100)
    
    def fly(self):
        self.pause = 0
        self.bird_rect = birds[self.flyIndex].get_rect(topleft = (self.x, self.y))

        # readjust hitbox
        self.bird_rect = self.bird_rect.inflate(-100, -100)

        game_screen.blit(birds[self.flyIndex], (self.x, self.y))
        self.x -= 20 # speed bird goes across the screen
        
        # flying animation (switch index continuously while blitting ^)
        self.flyIndex += 1
        if (self.flyIndex >= len(birds)):
            self.flyIndex = 0

        self.bird_rect = birds[self.flyIndex].get_rect(topleft = (self.x, self.y))

        # reset position when crosses left side of screen
        if self.x < -birds[self.flyIndex].get_width():
            self.x = 1200
            self.y = random.randint(50, 300)

        
new_dino = Dino()
new_ground = Ground()
new_cloud = Cloud()
new_cacti = Cacti()
new_birds = Bird()

while True:
    pygame.time.delay(50)
    # continually check if quit is called
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # close window after input received
            sys.exit() # ends code as well

    game_screen.fill((255, 255, 255)) # fills screen with white

    # moves ground as game goes along
    new_ground.scroll()

    # draws clouds on screen
    new_cloud.cloudDraw()

    # draws obstacles on screen
    new_cacti.obstacleDraw()
    new_birds.fly()

    # check continuously for collision between dinosaur and obstacle
    if new_dino.dino_rect.colliderect(new_cacti.small_rect) or new_dino.dino_rect.colliderect(new_cacti.big_rect) or new_dino.dino_rect.colliderect(new_birds.bird_rect):
        break

    keys = pygame.key.get_pressed() # obtains keys that are currently being pressed
    if keys[pygame.K_DOWN] and new_dino.jumpState == False: # if down is pressed, dino will duckState
        # update current state variables
        new_dino.duckState = True
        new_dino.runState = False
        new_dino.jumpState = False

        new_dino.duck()
    
    elif (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and new_dino.duckState == False:
        new_dino.jumpState = True
        new_dino.runState = False
        new_dino.duckState = False

        new_dino.jump()

    else: #"idle" state (i.e. keep running normally)
        new_dino.runState = True
        new_dino.duckState = False
        new_dino.jumpState = False

        new_dino.run()


    clock.tick(120)
    pygame.display.update()
