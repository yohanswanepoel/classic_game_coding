import pgzrun
from pgzhelper import *
from icecream import ic
import random
import os

DEBUG = os.getenv("DEBUG",False) 
if DEBUG:
    ic.enable()
else:
    ic.disable()

# ORIGINAL GAME SIZE
ORIGINAL_WIDTH = 600
ORIGINAL_HEIGHT = 600
SCREEN_RESIZE_FACTOR = 1.4  #For resizing the board and scaling everything as required

# Width and height of the screen
WIDTH = ORIGINAL_WIDTH * SCREEN_RESIZE_FACTOR
HEIGHT = ORIGINAL_HEIGHT * SCREEN_RESIZE_FACTOR
BACKGROUND_COLOUR = (199, 227, 255) # Colour is a dicationary (Red, Green, Blue) range 0-255

players_list = ['Nadia','Johan','Emily','Noah','Zechariah']  # Easy way to solve who is left

# WHEEL
SPIN_SPEED_MIN = 20
SPIN_SPEED_MAX = 35
SPIN_DIRECTION = -1
SPIN_FRICTION = 0.99
PIES = 5
DEGREES_PER_PI = int(360 / PIES)

SPIN_WHEEL_AXLE_POS =  (WIDTH / 2, HEIGHT / 2)

NOTIFY_FONT_SIZE = 40 * SCREEN_RESIZE_FACTOR
LIST_FONT_SIZE = 20 * SCREEN_RESIZE_FACTOR

WHEEL_AXCLE_RADIUS = 15 * SCREEN_RESIZE_FACTOR

wheel = Actor('wheel')
wheel.pos = (WIDTH / 2, HEIGHT / 2)
wheel.scale = 0.5 * SCREEN_RESIZE_FACTOR

# ARROW
ARROW_CIRCLE_RADIUS = 4 * SCREEN_RESIZE_FACTOR
arrow = Actor('arrow', anchor=('left', 'center'))
arrow.pos = (WIDTH / 2, int(HEIGHT * 0.1))
arrow.scale = 0.28 * SCREEN_RESIZE_FACTOR
arrow.angle = 270
ARROW_CIRCLE_POS = (WIDTH / 2, arrow.top + ARROW_CIRCLE_RADIUS * 2)

# GLOBAL: GAME BOARD VARIABLES 
previous_angle = 0
spin_speed = 0
current_angle = 0
clicks = 72
spin_wheel = False
winner = ""

winner_list = []

# GET winner
def get_winner(wheel_angle):
    actual_angle = wheel_angle % 360
    winner = ""
    pie = int(actual_angle / DEGREES_PER_PI)
    ic(players_list[pie])
    winner_temp = players_list[pie]
    if winner_temp in winner_list:
        winner = f"Spin again. {winner_temp} already listed"
        sounds.again.play()
    else:
        winner_list.append(winner_temp)
        game_done = ""
        if len(winner_list) == 4:
            remainder = list(set(players_list) - set(winner_list))
            winner_list.append(remainder[0])
            game_done = ". Game done"
            sounds.final.play()
        else:
            sounds.won.play()
        winner = f"Winner! {winner_temp} {game_done} "
    return winner

# The main draw function that runs every cycle
def draw():
    screen.clear()
    screen.fill(BACKGROUND_COLOUR)
    screen.draw.text(f"{winner}", (50, 30), color="orange", fontsize=NOTIFY_FONT_SIZE)
    screen.draw.text(f"Order: {' '.join(winner_list)}", (50, HEIGHT - 30 * SCREEN_RESIZE_FACTOR), color="orange", fontsize=LIST_FONT_SIZE)
    # Adds my elements to the screen
    wheel.draw()
    arrow.draw()
    screen.draw.filled_circle(ARROW_CIRCLE_POS,ARROW_CIRCLE_RADIUS,(255,215,0))
    screen.draw.filled_circle(SPIN_WHEEL_AXLE_POS,WHEEL_AXCLE_RADIUS,(255,215,0))

# This methods updates the canvas and characters
# Pygame Zero will call your update() function once every frame.
# Globals needed on pygame zero methods as they are part of the class
def update():
    global spin_wheel
    global spin_speed
    global SPIN_FRICTION
    global winner
    global previous_angle
    global current_angle
    global clicks
    if spin_wheel:
        spin_speed = spin_speed * SPIN_FRICTION
        adjust_angle = spin_speed * SPIN_DIRECTION 
        wheel.angle += adjust_angle
        current_angle += adjust_angle * -1
        if spin_speed < 0.10:
            spin_wheel = False
            winner = get_winner(wheel.angle)
        
        if (current_angle // clicks > previous_angle // clicks) and arrow.angle < 272: #Move the needle
            arrow.angle += 5
            sounds.click.play()

        previous_angle = current_angle
        # ic(arrow.angle, previous_angle, current_angle)
        if arrow.angle > 270:
            arrow.angle -= 1
        elif arrow.angle < 270:
            arrow.angle = 270


def on_mouse_down(button):
    global spin_wheel
    global spin_speed
    if button == mouse.LEFT and not spin_wheel:
        ic("Spinning Wheel")
        spin_speed = random.randint(SPIN_SPEED_MIN, SPIN_SPEED_MAX)
        spin_wheel = True
    elif button == mouse.RIGHT:
        ic("Stop Wheel")
        spin_wheel = False
