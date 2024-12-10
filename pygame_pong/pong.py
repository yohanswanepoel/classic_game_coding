import pygame
from pygame.locals import *
from sys import exit
# My local game properties
import properties as p
from icecream import ic
import random, math

###
### This version works by moving x and y coordinates
###

# pygame setup
global screen
pygame.init()

# ic.disable()

# Screen thigns
screen = pygame.display.set_mode((p.SCREEN_WIDTH, p.SCREEN_HEIGHT))
pygame.display.set_caption(p.GAME_TITLE)

# Clock object to help with framerate
clock = pygame.time.Clock()
dt = 0
shots = 0
player_list = pygame.sprite.Group()

game_running = False
score = ""
p1_score = 0
p2_score = 0

previous_shot = 0

# Ball out of bounds event
PLAYER_WINS = pygame.USEREVENT + 1

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


class UI():

    def __init__(self):
        # Font setup
        self.big_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.small_font = pygame.font.SysFont('Comic Sans MS', 15)

    def draw_start_game(self, screen):
        text_surface = self.big_font.render('Press Space to start \n "n" for new game', True ,"green", "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (p.SCREEN_WIDTH / 2, p.SCREEN_HEIGHT / 2)
        screen.blit(text_surface, text_rect)

    def draw_game_score(self, screen, score):
        text_surface = self.small_font.render(f'{score}', True, "green", "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (p.SCREEN_WIDTH / 2, 10)
        screen.blit(text_surface, text_rect)


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

    def stop(self):
        self.speed = 0
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0

    def launch(self):
        direction = random.choice([0, 1])
        start_angle = random.randint(p.BALL_START_ANGLE_MIN,p.BALL_START_ANGLE_MAX) # Angle from horizontal
        start_angle = start_angle + (180 * direction) # Go left or right
        self.angle = 360 + start_angle if start_angle < 0  else start_angle # stay within the 360 
        self.speed = p.BALL_START_VELOCITY
        # velocity math checks out here x*x+y*y = speed * speed
        self.vel_x = self.speed * math.cos(math.radians(self.angle)) 
        self.vel_y = self.speed * math.sin(math.radians(self.angle))

    #                     270
    #                      |
    # check bounds - 180 <- -> 0
    #                      | 
    #                      90 
    def change_direction(self, change_percentage, player):
        ic.disable()
        # VEL - is going up, VEL + is going down
        
        current_direction = "left" if 90 < self.angle < 270 else "right"
        paddle_spot = ""
        if abs(change_percentage) < 20:
            paddle_spot = "middle"
        else:
            paddle_spot = "bottom" if change_percentage > 0 else "top"

        # Collision logic
        if (current_direction == "right" and player == "p2") or (current_direction == "left" and player == "p1"):
            ic ("..... Current", change_percentage, current_direction, self.angle, paddle_spot)
            if current_direction == "right": # Current direction RIGHT
                if 0 < self.angle < 90:
                    self.angle = 180 - self.angle
                    ic("adjustment", self.angle)
                else:
                    self.angle = 180 + (360 - self.angle)
                    ic("adjustment", self.angle)
                if paddle_spot == "top":
                    ic("right", "top")
                    self.angle = self.angle + p.ANGLE_CHANGE_1
                    ic("adjustment", self.angle)
                elif paddle_spot == "bottom":
                    ic("right", "bottom")
                    self.angle = self.angle - p.ANGLE_CHANGE_1
                    ic("adjustment", self.angle)
            else: # Current direction LEFT
                if 90 < self.angle < 180:
                    self.angle = 180 - self.angle
                    ic("adjustment", self.angle)
                else: 
                    self.angle = 360 - (self.angle - 180)
                    ic("adjustment", self.angle)
                if paddle_spot == "top":
                    ic("left", "top")
                    self.angle = self.angle - p.ANGLE_CHANGE_1
                    ic("adjustment", self.angle)
                elif paddle_spot == "bottom":
                    ic("left", "bottom")
                    self.angle = self.angle + p.ANGLE_CHANGE_1
                    ic("adjustment", self.angle)

            self.angle = 360 + self.angle if self.angle < 0 else self.angle
            
            ic ("New Angle", self.angle)

  
    
    #                     270
    #                      |
    # check bounds - 180 <- -> 0
    #                      | 
    #                      90
    def update(self):
        self.vel_x = self.speed * math.cos(math.radians(self.angle)) 
        self.vel_y = self.speed * math.sin(math.radians(self.angle))
       
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
        if self.rect.y < 0:
            self.rect.y += 1
            if 180 < self.angle < 360:
                self.angle = 360 - self.angle
                
        if self.rect.y > (p.SCREEN_HEIGHT-p.BALL_HEIGHT):
            self.rect.y -= 1
            if 0 < self.angle < 180:
                self.angle = 360 - self.angle

        if not 0 < self.rect.x < (p.SCREEN_WIDTH-p.BALL_WIDTH):
            #ic("Point over")
            pygame.event.post(pygame.event.Event(PLAYER_WINS)) 
            # Need to notify game loop
        
    
p1 = Player("red", p.PADDLE_WIDTH, p.PADDLE_HEIGHT)
p1.rect.x, p1.rect.y = 10, p.SCREEN_HEIGHT / 2 - 50

p2 = Player("red", p.PADDLE_WIDTH, p.PADDLE_HEIGHT)
p2.rect.x, p2.rect.y = p.SCREEN_WIDTH - 30, p.SCREEN_HEIGHT / 2 - 50

ball = Ball("black", p.BALL_WIDTH, p.BALL_HEIGHT)
ball.rect.x, ball.rect.y = p.SCREEN_WIDTH /2, p.SCREEN_HEIGHT / 2

player_list.add(p1)
player_list.add(p2)

ui = UI()

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
            elif event.key == pygame.K_n:
                p1.move_up()
                ball.stop()
                ball.rect.x, ball.rect.y = p.SCREEN_WIDTH /2, p.SCREEN_HEIGHT / 2
                p1_score = 0
                p2_score = 0
                shots = 0
                game_running = False

            if (not game_running) and event.key == pygame.K_SPACE:
                ball.rect.x, ball.rect.y = p.SCREEN_WIDTH /2, p.SCREEN_HEIGHT / 2
                previous_shot = 0
                ball.launch()
                game_running = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                p2.stop()
            if event.key in (pygame.K_s, pygame.K_w):
                p1.stop()
        
        if event.type == PLAYER_WINS: 
            winner = ""
            if ball.rect.x < 0:
                winner = "Player 2"
                p2_score += 1
            else: 
                winner = "Player 1"
                p1_score += 1
            ball.stop()
            shots = 0
            ball.rect.x, ball.rect.y = p.SCREEN_WIDTH /2, p.SCREEN_HEIGHT / 2
            game_running = False
            

    if (shots != 0) and (previous_shot != shots) and (shots % p.INC_SPEED_SHOTS == 0 ):
        previous_shot = shots
        ball.speed += 1
    
    if pygame.sprite.collide_rect(ball, p1):
        center_offset = ball.rect.centery - p1.rect.centery
        ball.change_direction((center_offset / (p.PADDLE_HEIGHT / 2)) * 100, "p1")
        shots += 1
    elif pygame.sprite.collide_rect(ball, p2):
        center_offset = ball.rect.centery - p2.rect.centery
        ball.change_direction((center_offset / (p.PADDLE_HEIGHT / 2)) * 100, "p2")
        shots += 1
    
    player_list.update() # move players
    ball.update()
    # RENDER YOUR GAME HERE
    
    screen.fill("black")  # fill the screen with a color to wipe away anything from last frame

    player_list.draw(screen)    

    screen.blit(ball.image, (ball.rect.x, ball.rect.y))
    ui.draw_game_score(screen, f"Player 1: {p1_score} - Player 2: {p2_score}")
    if not game_running:
        ui.draw_start_game(screen)

    pygame.display.flip() 

    clock.tick(p.FPS)  # limits FPS to 60
