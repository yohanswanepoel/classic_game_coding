import pygame
from pygame.locals import *
from sys import exit
# My local game properties
import properties as p
from icecream import ic
import random, math


# pygame setup
global screen
pygame.init()

# Screen thigns
screen = pygame.display.set_mode((p.SCREEN_WIDTH, p.SCREEN_HEIGHT))
pygame.display.set_caption(p.GAME_TITLE)

# Clock object to help with framerate
clock = pygame.time.Clock()
dt = 0

player_list = pygame.sprite.Group()

# Class paddle
class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.vel_y = 0
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def stop(self):
        self.vel_y = 0

    def move_up(self):
        self.vel_y = -p.PADDLE_SPEED

    def move_down(self):
        self.vel_y = p.PADDLE_SPEED

    def update(self):
        self.rect.y += self.vel_y
        # check bounds
        if not 0 < self.rect.y < (p.SCREEN_HEIGHT-p.PADDLE_HEIGHT):
            self.rect.y -= self.vel_y

# Class ball
class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        pygame.draw.circle(self.image, "blue", (p.BALL_WIDTH / 2,p.BALL_HEIGHT / 2), p.BALL_HEIGHT / 2)
        self.speed = 0
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def launch(self):
        direction = random.choice([0, 1])
        start_angle = random.randint(p.BALL_START_ANGLE_MIN,p.BALL_START_ANGLE_MAX) # Angle from horizontal
        start_angle = start_angle + (180 * direction) # Go left or right
        self.angle = 360 + start_angle if start_angle < 0  else start_angle # stay within the 360 
        self.speed = p.BALL_START_VELOCITY
        # velocity math checks out here x*x+y*y = speed * speed
        self.vel_x = self.speed * math.cos(math.radians(self.angle)) 
        self.vel_y = self.speed * math.sin(math.radians(self.angle))
        # move_size = self.vel_x * self.vel_x + self.vel_y * self.vel_y
        ic(self.angle)
        
    def change_direction(self, change_percentage):
        # VEL - is going up, VEL + is going down
        if change_percentage < 0 and self.vel_y < 0: #Ball going up
            # TOP HALF, Reduce y velocity
            ic(change_percentage, self.vel_y)
            self.vel_y -= 1
            ic(self.vel_y)
        elif change_percentage < 0 and self.vel_y > 0: #Ball gonig down
            # TOP HALF
            ic(change_percentage, self.vel_y)
            self.vel_y -= 1
            ic(self.vel_y)
        if change_percentage > 0 and self.vel_y < 0: #Ball going up
            # BOTTOM HALF
            ic(change_percentage, self.vel_y)
            self.vel_y += 1
            ic(self.vel_y)
        elif change_percentage > 0 and self.vel_y > 0: #Ball gonig down
            # BOTTM HALF
            ic(change_percentage, self.vel_y)
            self.vel_y += 1
            ic(self.vel_y)
        elif self.vel_y == 0:
            self.vel_y = 1 if change_percentage else -1

        self.vel_x = self.vel_x * -1
        
    def update(self):
        current_pos_y = self.rect.y
        current_pos_x = self.rect.x
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        #                     270
        #                      |
        # check bounds - 180 <- -> 0
        #                      | 
        #                      90
        #if 0 > self.rect.y: # top of screen
        #    self.angle = 360 - self.angle

        #if self.rect.y > (p.SCREEN_HEIGHT-p.BALL_HEIGHT): # bottom of screen
        #    self.angle = 360 - self.angle
        #    ic("HEIGHT", self.angle)
            
        if not 0 < self.rect.y < (p.SCREEN_HEIGHT-p.BALL_HEIGHT):
            self.angle = 360 - self.angle
            self.vel_y = self.vel_y * -1
            ic(self.angle)
        # Needs to update to use angles
        
    
p1 = Player("red", p.PADDLE_WIDTH, p.PADDLE_HEIGHT)
p1.rect.x, p1.rect.y = 10, p.SCREEN_HEIGHT / 2 - 50

p2 = Player("red", p.PADDLE_WIDTH, p.PADDLE_HEIGHT)
p2.rect.x, p2.rect.y = p.SCREEN_WIDTH - 30, p.SCREEN_HEIGHT / 2 - 50

ball = Ball("black", p.BALL_WIDTH, p.BALL_HEIGHT)
ball.rect.x, ball.rect.y = p.SCREEN_WIDTH /2, p.SCREEN_HEIGHT / 2

player_list.add(p1)
player_list.add(p2)


while True:
    for event in pygame.event.get():
        # Check for game exit
        if event.type == pygame.QUIT:
            # uninitialise everything and quit
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                p2.move_down()
            elif event.key == pygame.K_UP:
                p2.move_up()
            if event.key == pygame.K_s:
                p1.move_down()
            elif event.key == pygame.K_w:
                p1.move_up()
            if event.key == pygame.K_SPACE:
                ball.rect.x, ball.rect.y = p.SCREEN_WIDTH /2, p.SCREEN_HEIGHT / 2
                ball.launch()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                p2.stop()
            if event.key in (pygame.K_s, pygame.K_w):
                p1.stop()
    
    if pygame.sprite.collide_rect(ball, p1):
        center_offset = ball.rect.centery - p1.rect.centery
        ball.change_direction((center_offset / (p.PADDLE_HEIGHT / 2)) * 100)
    elif pygame.sprite.collide_rect(ball, p2):
        center_offset = ball.rect.centery - p2.rect.centery
        ball.change_direction((center_offset / (p.PADDLE_HEIGHT / 2)) * 100)
    
    player_list.update() # move players
    ball.update()
    # RENDER YOUR GAME HERE
    
    screen.fill("black")  # fill the screen with a color to wipe away anything from last frame

    player_list.draw(screen)    

    screen.blit(ball.image, (ball.rect.x, ball.rect.y))
    
    pygame.display.flip() 

    clock.tick(p.FPS)  # limits FPS to 60
