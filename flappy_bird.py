import pygame, sys
import random
import time
import threading


game_over = False

#initialize pygame
pygame.init()
clock = pygame.time.Clock()

#set screen up
width = 288
height = 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        #intialize superclass (pygame.sprite.Sprite) by calling the superclass constructor
        super().__init__()
        #make a sprites array that adds each image to the array for animation
        self.sprites = []
        self.sprites.append(pygame.image.load('C:\\Users\\willb\OneDrive\\Desktop\python stuff\\flappy_bird_project\\flappy-bird-assets-master\\sprites\\yellowbird-midflap.png'))
        self.sprites.append(pygame.image.load('C:\\Users\\willb\\OneDrive\\Desktop\\python stuff\\flappy_bird_project\\flappy-bird-assets-master\\sprites\\yellowbird-downflap.png'))
        self.sprites.append(pygame.image.load('C:\\Users\\willb\\OneDrive\\Desktop\\python stuff\\flappy_bird_project\\flappy-bird-assets-master\\sprites\\yellowbird-upflap.png'))
        self.current_sprite = 0
        #set current image being blitted to the screen to the current sprite index
        self.image = self.sprites[self.current_sprite]
        #make the image a shape object so it can move 
        self.rect = self.image.get_rect()
        #center the player image at the x and y coordinates
        self.rect.center = [x,y]
        self.x = x
        self.y = y
        self.speed = 5
        self.paused = True
        self.game_started = False
    def handle_keys(self):
        #get key pressed and store it in the key variable
        key = pygame.key.get_pressed()
        
        #if space key is pressed have the bird fly up
        if key[pygame.K_SPACE] and self.paused == False: 
                self.speed = 10
                self.rect.y -= self.speed*2
                print(f"space pressed, unpaused,{self.paused}")
                print(self.speed)
        #if the game is not paused then have the bird fall down
    def checkForOffScreen(self):
            global game_over
            if self.rect.y>=512 and not game_over:
                #if y position is greater than the bottom of the window, blit a game over image to the screen. 
                game_over = pygame.image.load('C:\\Users\\willb\\OneDrive\\Desktop\\python stuff\\flappy_bird_project\\flappy-bird-assets-master\\sprites\\gameover.png')
                screen.blit(game_over,(0,0))
                pygame.display.flip()
                clock.tick(60)
                print("flipped")
                game_over = True
            elif self.rect.y<=10:
                 self.speed -= self.speed

    def update(self):
        #increment the current sprite index by 1
        self.current_sprite += 1

        #if the current sprite index is greater than the number of sprites, reset the current sprite index to zero
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        #set the current image to the current sprite index
        self.image = self.sprites[self.current_sprite]

        #if the game is paused leave the current sprite at index zero
        if self.paused == True:
            self.current_sprite = 0
            self.speed = 0
        #else if the game is not paused then increment the bird speed
        else:
            self.speed += 1
            print(f"self.speed is {self.speed}")
            self.rect.y += self.speed


class Pipe(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         self.x = 218
         self.separator = 100
         self.top_height = random.randint(0,256-self.separator)
         self.bottom_height = random.randint(400,512+self.separator)
         self.y = self.bottom_height
         self.image = pygame.image.load('C:\\Users\\willb\\OneDrive\\Desktop\\python stuff\\flappy_bird_project\\flappy-bird-assets-master\\sprites\\pipe-green.png').convert()
         self.rect = self.image.get_rect()
         self.rect.center = [self.x,self.y]



#load background image in 
background = pygame.image.load('C:\\Users\\willb\\OneDrive\\Desktop\\python stuff\\flappy_bird_project\\flappy-bird-assets-master\sprites\\background-day.png').convert()

#load bird image in 
bird = Player(width/2,height/2)
bird_group = pygame.sprite.Group()
bird_group.add(bird)
last_pipe_spawn_time = time.time()
pipe_spawn_interval = 2
pipe_group = pygame.sprite.Group()
pipes = [] #declare a pipes list global variable

#if the game is not yet over, handle keys and update the screen, and set the framerate to 30fps
def gameNotOver():
     bird.handle_keys()
     bird.update()
     bird.checkForOffScreen()
     clock.tick(35)

#else blit game over to the screen, set the framerate to 1 fps and update the screen
def gameIsOverNow():
     game_over = pygame.image.load('C:\\Users\\willb\\OneDrive\\Desktop\\python stuff\\flappy_bird_project\\flappy-bird-assets-master\\sprites\\gameover.png').convert()
     screen.blit(game_over,(0,0))
     pygame.display.flip()
     clock.tick(1)

#function for spawning pipes into the game
def spawnPipes():
    pipe = Pipe()  # Create a new instance of the Pipe class
    pipe_group.add(pipe)  # Add the pipe to the pipe_group


#function for updating pipes
def updatePipes():
      for pipe in list(pipe_group):
        pipe.rect.x -= 10  # Move each pipe 20 to the left in X value
        if pipe.rect.x < -pipe.rect.width:  # Remove pipe if it's off the screen
            pipe_group.remove(pipe)
        pipe_group.draw(screen)  # Draw pipes to the screen


#main loop
while True:
    current_time = time.time()
    for event in pygame.event.get():
        #quit if the player exits the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        #if the game hasnt started and the F key is pressed set the pause state to False and start the game
        if not bird.game_started and event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            bird.paused = False
            bird.game_started = True

            print("F key is pressed, game started and unpaused")


    screen.blit(background, (0,0))

    #if the game is not yet over, call the gameNotOver function
    if not game_over:
         gameNotOver()
         updatePipes()
         if bird.game_started and current_time - last_pipe_spawn_time >= pipe_spawn_interval:
            last_pipe_spawn_time = current_time
            spawnPipes()

    bird_group.draw(screen)

    #else blit game over to the screen, call the gameIsOverNow function
    if game_over:
         gameIsOverNow()
    


    #draw the sprites to the screen
    pygame.display.flip()