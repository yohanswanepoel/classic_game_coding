"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from random import randint

SCALE = 2

SCREEN_WIDTH = 400 * SCALE
SCREEN_HEIGHT = 400 * SCALE
SNAKE_SIZE = 10 * SCALE
BLOCK_SIZE = SNAKE_SIZE
SCREEN_TITLE = "Snake"
ROWS = SCREEN_HEIGHT // SNAKE_SIZE
COLUMNS = SCREEN_WIDTH // SNAKE_SIZE
COIN_RADIUS = 4 * SCALE

# SNAKE_COLUMN_SPEED = 1/5 * SCALE # SNAKE will take 5 tics to move a block
SNAKE_COLUMN_SPEED = 1
SNAKE_SPEED = SNAKE_COLUMN_SPEED * 10

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

# mPos.y += velocityScale * mVelocity * deltaTime
# needs to be fullscreen and then get size of screen
# determine ratios from there

class SnakePart:
    def __init__(self, row, col, colour, direction):
        self.row = row
        self.col = col
        self.colour = colour
        self.direction = direction
        self.move_size = None
        self.x = self.col * SNAKE_SIZE
        self.y = self.row * SNAKE_SIZE

    def draw(self):
        self.x = self.col * SNAKE_SIZE + SNAKE_SIZE / 2
        self.y = self.row * SNAKE_SIZE + SNAKE_SIZE / 2
        arcade.draw_rectangle_filled(
            self.x, self.y,
            SNAKE_SIZE, SNAKE_SIZE, self.colour
        )

    def update_position(self):
        pass

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.snake = None
        self.snake_2 = None
        self.head_row = 20
        self.head_col = 20
        self.p1_direction = None
        self.p2_direction = None
        self.coin_row = None
        self.coin_col = None
        self.add_tail = None
        self.add_tail_2 = None
        self.multi_player = None
        self.player_crash = None
        arcade.set_background_color(arcade.color.AMAZON)


        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.snake = []
        self.snake_2 = []
        # SETUP SNAKE 1
        self.p1_direction = RIGHT
        self.multi_player = True
        self.player_crash = True
        self.add_tail = False
        self.snake.append(SnakePart(15,20, arcade.color.BLUE, RIGHT))
        self.snake.append(SnakePart(15, 19, arcade.color.GREEN, RIGHT))
        self.snake.append(SnakePart(15, 18, arcade.color.BLUE, RIGHT))
        self.snake.append(SnakePart(15, 17, arcade.color.BLUE, RIGHT))
        # SETUP SNAKE 2
        if self.multi_player:
            self.p2_direction = LEFT
            self.add_tail_2 = False
            self.snake_2.append(SnakePart(25, 20, arcade.color.GREEN, RIGHT))
            self.snake_2.append(SnakePart(25, 21, arcade.color.BLUE, RIGHT))
            self.snake_2.append(SnakePart(25, 22, arcade.color.GREEN, RIGHT))
            self.snake_2.append(SnakePart(25, 23, arcade.color.GREEN, RIGHT))
        self.coin_position()

    def coin_position(self):
        self.coin_row = randint(1, ROWS - 1)
        self.coin_col = randint(1, COLUMNS - 1)\

    def draw_snake(self, snake):
        for part in snake:
            part.draw()

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.draw_snake(self.snake)
        if self.multi_player:
            self.draw_snake(self.snake_2)

        arcade.draw_circle_filled(self.coin_col * BLOCK_SIZE + BLOCK_SIZE / 2,
                                  self.coin_row * BLOCK_SIZE + BLOCK_SIZE / 2,
                                  COIN_RADIUS, arcade.color.RED)

        # Call draw() on all your sprite lists below

    def move_snake(self, direction, snake, player):
        prev_part_row = -1
        prev_part_col = -1
        for part in snake:
            if prev_part_row == -1:
                prev_part_row = part.row
                prev_part_col = part.col
                if direction == RIGHT:
                    part.col += 1
                elif direction == LEFT:
                    part.col -= 1
                elif direction == UP:
                    part.row += 1
                elif direction == DOWN:
                    part.row -= 1
            else:
                tmp_part_row = part.row
                tmp_part_col = part.col
                part.col = prev_part_col
                part.row = prev_part_row
                prev_part_row = tmp_part_row
                prev_part_col = tmp_part_col
        # NEED to check snake 1 or 2
        if player == 1:
            if self.add_tail:
                snake.append(SnakePart(prev_part_row, prev_part_col, arcade.color.BLUE, RIGHT))
                self.add_tail = False
        elif player == 2:
            if self.add_tail_2:
                snake.append(SnakePart(prev_part_row, prev_part_col, arcade.color.GREEN, RIGHT))
                self.add_tail_2 = False



    def check_boundaries(self, snake, player):
        p_row = snake[0].row
        p_col = snake[0].col
        if p_row < 0 or p_col < 0 or p_row > ROWS or p_col > COLUMNS:
            print(f"GAME OVER! P{player} out of bounds")
            self.setup()

    def collision_self_apple(self, snake, player):
        p_row = snake[0].row
        p_col = snake[0].col
        # COIN COLLISION
        if p_row == self.coin_row and p_col == self.coin_col:
            print("boom")
            # Span a new coin
            self.coin_position()
            # Add tail to snake - it only gets the snake on next game loop
            if player == 1:
                self.add_tail = True
            elif player == 2:
                self.add_tail_2 = True
        else: # SELF COLLISION
            for part in snake[1:]: # Ignore the first one
                if p_row == part.row and p_col == part.col:
                    print(f"ouch!! Player{player} died")
                    self.setup()

    def collision_snakes(self):
        # CHECK Snake on snake collision
        p1_row = self.snake[0].row
        p1_col = self.snake[0].col
        p2_row = self.snake_2[0].row
        p2_col = self.snake_2[0].col
        if p1_row == p2_row and p1_col == p2_col:
            print("TIE")
            self.setup()

        for part in self.snake_2[1:]:  # Ignore the first one
            if p1_row == part.row and p1_col == part.col:
                print(f"ouch!! Player1 died")
                self.setup()

        for part in self.snake[1:]:  # Ignore the first one
            if p2_row == part.row and p2_col == part.col:
                print(f"ouch!! Player2 died")
                self.setup()

    def on_update(self, delta_time):
        """
        Need to move by row and column and then use the linear interpolation to make it smooth
        """
        self.check_boundaries(self.snake, 1)
        if self.multi_player:
            self.check_boundaries(self.snake_2, 2)
            self.collision_self_apple(self.snake_2, 2)
            self.collision_snakes()
        self.collision_self_apple(self.snake, 1)

        self.move_snake(self.p1_direction, self.snake, 1)
        if self.multi_player:
            self.move_snake(self.p2_direction, self.snake_2, 2)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # cannot go in opposite direction
        if key == arcade.key.UP and not self.p1_direction == DOWN:
            self.p1_direction = UP
        elif key == arcade.key.RIGHT and not self.p1_direction == LEFT:
                self.p1_direction = RIGHT
        elif key == arcade.key.DOWN and not self.p1_direction == UP:
                self.p1_direction = DOWN
        elif key == arcade.key.LEFT and not self.p1_direction == RIGHT:
                self.p1_direction = LEFT

        if key == arcade.key.W and not self.p2_direction == DOWN:
            self.p2_direction = UP
        elif key == arcade.key.D and not self.p2_direction == LEFT:
                self.p2_direction = RIGHT
        elif key == arcade.key.S and not self.p2_direction == UP:
                self.p2_direction = DOWN
        elif key == arcade.key.A and not self.p2_direction == RIGHT:
                self.p2_direction = LEFT

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.set_update_rate(1/15)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()