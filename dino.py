import pygame
import sys

from pygame.constants import K_SPACE, K_UP

pygame.init()

# set title and image for window 
pygame.display.set_caption("Chrome Dino Game")
dino_icon = pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\dino.jpg')
pygame.display.set_icon(dino_icon)

game_screen = pygame.display.set_mode((1100, 800)) # creates display
ground = pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\Assets\\Other\\Track.png')

playerRun = [pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\Assets\\Dino\DinoRun1.png'),
             pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\Assets\\Dino\DinoRun2.png')]

playerDuck = [pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\Assets\\Dino\DinoDuck1.png'),
              pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\Assets\\Dino\DinoDuck2.png')]

playerJump = pygame.image.load('C:\\Users\\Owner\\Documents\\Python Projects\\Dino Run\\Assets\\Dino\DinoJump.png')
# used for fps
clock = pygame.time.Clock()

# class for Dinosaur object
class Dino:
    runIndex = 0
    duckIndex = 0

    jumpState = False
    runState = True
    duckState = False

    dinoGravity = 10
    dinoY = 300

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
    
    def duck(self):
        game_screen.blit(playerDuck[self.duckIndex], (80, 340))

        self.duckIndex += 1
        if (self.duckIndex >= len(playerDuck)):
            self.duckIndex = 0
    
    def jump(self):
        if self.dinoGravity >= -10:
            self.dinoY -= (self.dinoGravity * abs(self.dinoGravity)) * 0.4
            self.dinoGravity -= 1
        else:
            self.dinoGravity = 10
            self.jumpState = False
        game_screen.blit(playerJump, (80, self.dinoY))
    

groundSpeed = 4
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

new_dino = Dino()
new_ground = Ground()

while True:
    pygame.time.delay(100)
    # continually check if quit is called
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # close window after input received
            sys.exit() # ends code as well

    game_screen.fill((255, 255, 255)) # fills screen with white

    # moves ground as game goes along
    new_ground.scroll()

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
