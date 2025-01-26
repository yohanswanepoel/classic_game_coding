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
        self.head_row = 20
        self.head_col = 20
        self.p1_direction = None
        self.p2_direction = None
        self.coin_row = None
        self.coin_col = None
        self.add_tail = None
        arcade.set_background_color(arcade.color.AMAZON)


        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.snake = []
        self.p1_direction = RIGHT
        self.add_tail = False
        self.snake.append(SnakePart(20,20, arcade.color.BLUE, RIGHT))
        self.snake.append(SnakePart(20, 19, arcade.color.GREEN, RIGHT))
        self.snake.append(SnakePart(20, 18, arcade.color.BLUE, RIGHT))
        self.snake.append(SnakePart(20, 17, arcade.color.BLUE, RIGHT))
        self.coin_position()

    def coin_position(self):
        self.coin_row = randint(1, ROWS - 1)
        self.coin_col = randint(1, COLUMNS - 1)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        for part in self.snake:
            part.draw()

        arcade.draw_circle_filled(self.coin_col * BLOCK_SIZE + BLOCK_SIZE / 2,
                                  self.coin_row * BLOCK_SIZE + BLOCK_SIZE / 2,
                                  COIN_RADIUS, arcade.color.RED)

        # Call draw() on all your sprite lists below

    def move_snake(self, direction):
        prev_part_row = -1
        prev_part_col = -1
        for part in self.snake:
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
        if self.add_tail:
            self.snake.append(SnakePart(prev_part_row, prev_part_col, arcade.color.BLUE, RIGHT))
            self.add_tail = False


    def check_boundaries(self):
        p1_row = self.snake[0].row
        p1_col = self.snake[0].col
        if p1_row < 0 or p1_col < 0 or p1_row > ROWS or p1_col > COLUMNS:
            print("GAME OVER!")
            self.setup()

    def check_collision(self):
        p1_row = self.snake[0].row
        p1_col = self.snake[0].col
        # COIN COLLISION
        if p1_row == self.coin_row and p1_col == self.coin_col:
            print("boom")
            # Span a new coin
            self.coin_position()
            # Add tail to snake - it only gets the snake on next game loop
            self.add_tail = True
        else: # SELF COLLISION
            for part in self.snake[1:]: # Ignore the first one
                if p1_row == part.row and p1_col == part.col:
                    print("ouch!!")
                    self.setup()



    def on_update(self, delta_time):
        """
        Need to move by row and column and then use the linear interpolation to make it smooth
        """
        self.check_boundaries()
        self.check_collision()
        self.move_snake(self.p1_direction)

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