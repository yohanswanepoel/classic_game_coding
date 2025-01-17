# Basic arcade program
# Displays a white window with a blue circle in the middle

# Imports
import arcade
from typing import Optional
import pyglet
import random

# Arcade x, y starts from bottom left (other engines often from top left)
# Gravity
GRAVITY = 250

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
BOOST_FORCE = 1000
DIRECTTION_BOOST_FORCE = 300
## PLAYER
CHARACTER_SCALING = 1.7
PLAYER_MASS = 2.0
PLAYER_FRICTION = 1.0
# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1000
PLAYER_STARTING_FUEL = 300
SURFACE_FRICTION = 0.7

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_CENTER_X = SCREEN_WIDTH / 2
SCREEN_CENTER_Y = SCREEN_HEIGHT / 2
SCREEN_TITLE = "Lumar Lander 2024 - Python Arcade"
RADIUS = 20
PLAYER_START_X = SCREEN_CENTER_X
PLAYER_START_Y = SCREEN_HEIGHT - 80

LEFT = 2
RIGHT = 1
STRAIGHT = 0
EXPLOSION_TEXTURE_COUNT = 60

class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()



# Classes
class Lunar_Game(arcade.Window):
    # Main welcome window

    def __init__(self):
        # call parent class
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.moon_list: Optional[arcade.SpriteList] = None
        # Player sprite
        self.player_sprite: Optional[arcade.Sprite] = None
        self.crash_sound = None
        self.boost_sound = None
        self.left_right = None  
        self.win_sound = None
        self.good_landing: bool = None
        self.level = 1
        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.boost: bool = False
        self.player_direction = STRAIGHT
        self.sound_player: Optional[pyglet.media.player.Player] = None
        self.moon_surface = None
        self.landing_velocity = None
        self.game_started = None
        self.explode = False
        self.substrate: Optional[arcade.SpriteList] = None
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        arcade.set_background_color(arcade.color.BLACK)
        # takes too long and would cause the game to pause.
        self.explosions_list = None
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)


    def setup(self):
        # Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.moon_list = arcade.SpriteList()
        self.level = 6
        
        self.boost_sound = arcade.load_sound("sounds/drive.wav")
        self.win_sound = arcade.load_sound("sounds/win.wav")
        self.crash_sound = arcade.load_sound("sounds/bomb.wav")
        self.explosions_list = arcade.SpriteList()
        
        self.position_player()
        
        # Define surface
        if self.moon_surface is None:
            self.moon_surface = Moon()
                
        self.moon_list = None
        self.moon_list = self.moon_surface.generate_surface(self.level)
        self.substrate = self.moon_surface.get_substrate()
        
        self.player_sprite.fuel = PLAYER_STARTING_FUEL
        self.game_started = False
        
        
    def position_player(self):
        if self.player_sprite is None:
            self.player_list = arcade.SpriteList()
            self.player_sprite = Lunar_Sprite()
            
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        if len(self.player_list) == 0:
            self.player_list.append(self.player_sprite)
       
    def start_game(self):
        ## Physics Engine
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.fuel = PLAYER_STARTING_FUEL
        self.player_sprite.landed = False
        #self.position_player()
        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITY)
        self.good_landing = False
        self.game_started = True
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)

        # Player physics
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
        
        # surface physics
        self.physics_engine.add_sprite_list(sprite_list=self.moon_list,
                                            friction=SURFACE_FRICTION,
                                            collision_type="surface",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)
        
        # Collision handler
        def lander_on_surface_handler(player_sprite, surface_sprite, _arbiter, _space, _data):
            if self.player_sprite.landed == False:
                #print(player_sprite.get_velocity(self.physics_engine))
                self.velocity = player_sprite.previous_velocity
                if surface_sprite.direction != 0:
                    self.good_landing = False
                else:
                    if player_sprite.previous_velocity > -100:
                        self.good_landing = True
                    else:
                        self.good_landing = False
                        
                if self.good_landing:
                    arcade.play_sound(self.win_sound)
                else:
                    arcade.play_sound(self.crash_sound)
                    self.explode = True
                    
                self.player_sprite.landed = True
                self.game_started = False
                
            
        self.physics_engine.add_collision_handler("player","surface", post_handler=lander_on_surface_handler)
        
        
        
    def on_update(self, delta_time):
        # All the logic to move, and the game logic goes here.
        # Normally, you'll call update() on the sprite lists that need it.
        self.explosions_list.update()
        
        if self.explode:
            explosion = Explosion(self.explosion_texture_list)

            # Move it to the location of the coin
            explosion.center_x = self.player_sprite.center_x
            explosion.center_y = self.player_sprite.center_y + 30

            # Call update() because it sets which image we start on
            explosion.update()

            # Add to a list of sprites that are explosions
            self.explosions_list.append(explosion)
            self.explode = False
        
        if self.game_started:
            
            if self.player_out_of_bounds(self.player_sprite):
                self.game_started = False
                self.player_sprite.landed = True
                self.explode = True
                arcade.play_sound(self.crash_sound)
            
            if self.player_sprite.has_fuel():
                if self.boost:
                    self.player_sprite.boost_animation()
                    force = (0, BOOST_FORCE)
                    self.apply_boost(force)
            
                if self.player_direction == LEFT:
                    force = (-DIRECTTION_BOOST_FORCE, 0)
                    self.apply_boost(force)
                    
                if self.player_direction == RIGHT:
                    force = (DIRECTTION_BOOST_FORCE, 0)
                    self.apply_boost(force)
                    
                if not self.boost and self.player_direction == STRAIGHT:
                    self.no_boost()
            else:
                self.no_boost()
                    
            if not self.player_sprite.landed:
                self.player_sprite.previous_velocity = self.player_sprite.get_velocity(self.physics_engine)
                
            self.physics_engine.step()
        
    def apply_boost(self, force):
        self.physics_engine.apply_force(self.player_sprite, force)
        self.play_boost_sound()
        if self.player_sprite.fuel > 0:
            self.player_sprite.fuel -= 1
        
    def no_boost(self):
        self.player_sprite.normal_animation()
        if self.sound_player:
            arcade.stop_sound(self.sound_player)
            self.sound_player = None
            
    def player_out_of_bounds(self, player):
        if player.center_x < 0 or player.center_x > SCREEN_WIDTH:
            return True
        if player.center_y < 0:
            return True
        return False
        
    def on_draw(self):
        # Clear screen and start drawing
        arcade.start_render()
        
        # first draw boundaries
        arcade.draw_rectangle_outline(SCREEN_CENTER_X, SCREEN_CENTER_Y,
                                      SCREEN_WIDTH - 2, SCREEN_HEIGHT - 2,
                                      arcade.csscolor.WHITE, 1)
        # draw sprites
        self.moon_list.draw()
        self.substrate.draw()
        if not self.player_sprite.landed or self.good_landing:
            self.player_list.draw()
        self.explosions_list.draw()
        
        #
        # draw UI elements
        #
        velocity = 0
        if self.game_started:
            velocity = self.player_sprite.get_velocity(self.physics_engine)
            
        velocity_text = f"Speed: {velocity:.2f}"
        fuel_text = f"Fuel: {self.player_sprite.fuel}"
        
        arcade.draw_text(velocity_text, 10, SCREEN_HEIGHT - 40, arcade.csscolor.WHITE, 12,)
        self.draw_speed_guage(velocity, 300, -300, -100, -60, 10, SCREEN_CENTER_Y, 15, SCREEN_CENTER_Y - 50)
        
        arcade.draw_text(fuel_text, 10 , SCREEN_HEIGHT - 20, arcade.csscolor.WHITE, 12,)
        self.draw_fuel_guage(self.player_sprite.fuel, PLAYER_STARTING_FUEL, 0, 50, True, 
                        90, SCREEN_HEIGHT - 20, 150, 10)
        
        if self.good_landing:
            win_loose = "WINNER!"
        elif self.good_landing == False:
            win_loose = "TRY AGAIN"
        else:
            win_loose = ""
            
        if not self.game_started:
            start_text = f" {win_loose} velocity: {self.player_sprite.previous_velocity:.2f}"
            arcade.draw_text(start_text, SCREEN_CENTER_X - 100, SCREEN_CENTER_Y, arcade.csscolor.WHITE, 18,)
            self.draw_speed_guage(self.player_sprite.previous_velocity, 300, -300, -100, -60, 10, SCREEN_CENTER_Y, 15, SCREEN_CENTER_Y - 50)
            
            start_text = "[s] to start the game. [r] to reload surface"
            arcade.draw_text(start_text, SCREEN_CENTER_X - 200, SCREEN_CENTER_Y - 40, arcade.csscolor.WHITE, 18,)
            
        
        
    def draw_speed_guage(self, current, max, min, cut_off, draw_mid, x, y, width, height):
        
        # max translate to width
        factor = max / height
        # divide by 2 as we are starting in the middle
        current_level = (current / factor) / 2
        arcade.draw_xywh_rectangle_outline(x, y,
                                      width, height,
                                      arcade.csscolor.WHITE, 1)
    
        colour = arcade.csscolor.GREEN
        if current > 0:
            colour = arcade.csscolor.BLUE
        elif current < draw_mid:
            colour = arcade.csscolor.ORANGE
        elif current < cut_off:
            colour = arcade.csscolor.RED
        # get center of guage
        guage_center_y = y + (height / 2)
        arcade.draw_xywh_rectangle_filled(x, guage_center_y,
                                      width-1, current_level,
                                      colour)
        
    
    def draw_fuel_guage(self, current, max, min, cut_off, draw_mid, x, y, width, height):
        
        # max translate to width
        factor = max / width
        current_level = current / factor
        arcade.draw_xywh_rectangle_outline(x, y,
                                      width, height,
                                      arcade.csscolor.WHITE, 1)
    
        colour = arcade.csscolor.GREEN
        if draw_mid and current < max  / 2:
            colour = arcade.csscolor.ORANGE
        if current < cut_off:
            colour = arcade.csscolor.RED
        arcade.draw_xywh_rectangle_filled(x, y,
                                      current_level, height-1,
                                      colour)
        
        
        

    def on_key_press(self, key, key_modifiers):
        # Called whenever a key on the keyboard is pressed.
        # For a full list of keys, see: https://api.arcade.academy/en/latest/arcade.key.html
        if key == arcade.key.SPACE:
            self.boost = True
            
        if key == arcade.key.LEFT:
            self.player_direction = LEFT
        elif key == arcade.key.RIGHT:
            self.player_direction = RIGHT
            
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            
        if key == arcade.key.S:
            self.start_game()
            
        if key == arcade.key.R:
            self.setup()

    def on_key_release(self, key, key_modifiers):
        # Called whenever the user lets off a previously pressed key.
        if key == arcade.key.SPACE:
            self.boost = False
            
        if key == arcade.key.LEFT or key == arcade.key.RIGHT :
            self.player_direction = STRAIGHT
            
    def play_boost_sound(self):
        if not self.sound_player:
            self.sound_player = arcade.play_sound(self.boost_sound)

    
class Lunar_Sprite(arcade.Sprite):

    def __init__(self):
        # Let parent initialize
        super().__init__()
        self.textures: Optional[list[arcade.texture.Texture]] = None
        self.name = "Player 1" 
        self.scale = CHARACTER_SCALING
        self.fuel = PLAYER_STARTING_FUEL
        self.landed = False
        
        self.textures = arcade.load_spritesheet(
                file_name = "images/player.png",
                sprite_width = 20, sprite_height = 60, columns = 3, count = 3,
                margin = 0 
            ) # List[arcade.texture.Texture]
        
        self.texture = self.textures[0]
        
        self.hit_box = self.texture.hit_box_points
        self.previous_velocity = 0
    
    def boost_animation(self):
        self.texture = self.textures[2] 
        
    def normal_animation(self):
        self.texture = self.textures[0]
        
    def has_fuel(self):
        return True if self.fuel > 0 else False
    
    def get_velocity(self, physics_engine):
        return physics_engine.get_physics_object(self).body.velocity.y
    

class Moon():
    def __init__(self):
        super().__init__()
        self.substrate = None
        # Blocks are 40px wide, screen width = 800 so need 20 blocks
        #self.surface = arcade.SpriteList()
    
    # needs a generator with a percentage of flat vs hills
    # hills need to consider x, y as well... e.g. if first on slopes up then 
    # next should be one block 
    
    def get_substrate(self):
        return self.substrate
    
    def create_level_distribution(self, level):
        # setup blocks
        # percentage flat per level... 1 = 80%, 2 = 60%, 3 = 40%, 4 = 20%, 5 = 10% (rest)
        tmp_list = []
        if level > 6:
            level = 6
        level_adjuster = 2 * (level + 1)
        for i in range (21):
            if i < level_adjuster / 2:  # DOWN RIGHT
                sprite = Temp_Block()
                sprite.direction = -1
            elif level_adjuster / 2 <= i < level_adjuster : # DOWN LEFT
                sprite = Temp_Block()
                sprite.direction = 1
            else:
                sprite = Temp_Block()
                sprite.direction = 0

            tmp_list.append(sprite)
        
        # Shuffle blocks
        random.shuffle(tmp_list)
        return tmp_list
    
    def presentation_adjustment_surface(self, tmp_list):
        lowest = 0
        current_height = 0
        previous_height = 0
        i = 0
        # now do adjustments
        for t_sprite in tmp_list:
            current_height += t_sprite.direction
                
            if current_height < lowest:
                lowest = current_height
                
            t_sprite.col = i
            t_sprite.row = previous_height
            if t_sprite.direction == 1:
                t_sprite.row += 1
            previous_height = current_height
            i += 1
        
        adjuster = 0
        if lowest < 0:
            adjuster = (lowest * -1) + 1
        if lowest == 0:
            adjuster = 1
            
        return adjuster
        
    def generate_surface(self, level):
        tmp_list = self.create_level_distribution(level)
        
        adjuster = self.presentation_adjustment_surface(tmp_list)
        
        # Load sprites to display
        i = 0
        surface = arcade.SpriteList()
        self.substrate = arcade.SpriteList()
        for t_sprite in tmp_list:
            #print(sprite.original_index)
            if t_sprite.direction == 0:  
                sprite = Moon_Block("images/flat.png")
            elif t_sprite.direction == -1:
                sprite = Moon_Block("images/right.png")
            elif t_sprite.direction == 1:
                sprite = Moon_Block("images/left.png")
            sprite.row = t_sprite.row + adjuster
            sprite.center_y = (sprite.row * 40) - 20
            sprite.direction = t_sprite.direction
            for x in range (sprite.row): # create another sprite that lives in the substrate
                core = Moon_Block("images/core.png")
                core.center_x = (i * 40) - 20
                core.center_y = ((x) * 40) - 20
                self.substrate.append(core)
                
            sprite.center_x = (i * 40) - 20
            sprite.col = t_sprite.col
            surface.append(sprite)
            i += 1
            
        return surface
        
class Temp_Block():
    def __init__(self):
        self.direction = 0
        self.col = 0 
        self.row = 0
        self.original_index = 0
        
class Moon_Block(arcade.Sprite):
    def __init__(self,image):
        super().__init__(image)
        self.row = 0
        self.col = 0
        self.direction = 0
        self.original_index = 0
    
def main():
    app = Lunar_Game()
    app.setup()
    arcade.run()

# Main Function
if __name__ == "__main__":
    main()
    