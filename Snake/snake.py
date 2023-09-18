import random
import time

import arcade
from PIL import Image

# Set how many rows and columns we will have
ROW_COUNT = 20
COLUMN_COUNT = 20

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30  # 30
HEIGHT = 30  # 30

# This sets the margin between each cell
# and on the edges of the screen.
BORDER_MARGIN = 5
CELL_MARGIN = 2

# Do the math to figure out our screen dimensions
MAIN_BOARD_WIDTH = BORDER_MARGIN + (WIDTH + CELL_MARGIN) * COLUMN_COUNT
SCREEN_WIDTH = MAIN_BOARD_WIDTH + BORDER_MARGIN
SCREEN_HEIGHT = (HEIGHT + CELL_MARGIN) * ROW_COUNT + BORDER_MARGIN
SCREEN_TITLE = "SNAKE"

# Speed of the blocks falling down
SPEED = 60
SPEED_BOOST = 200

COLORS = [
    (0,   0,   0, 255),  # black
    (255, 0,   0, 255),  # red
    (0,   150, 0, 255),  # green
    (0,   0,   255, 255),  # blue
    (255, 120, 0, 255),  # orange
    (255, 255, 0, 255),  # yellow
    (180, 0,   255, 255),  # purple
    (0,   220, 220, 255),  # light blue
    (150, 150, 150, 255)  # black
]


class Snake(object):
    def __init__(self):
        self.coordinates = [(0, 2), (0, 1), (0, 0)]
        self.colors = [random.randint(1, 8) for i in range(3)]

    def move(self):
        self.coordinates.pop()

        head = self.coordinates[0]
        self.coordinates.insert(0, (head[0], head[1] + 1))


class MySnake(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Set up the application. """

        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.board_sprite_list = None
        self.snake = Snake()

    def setup(self):
        self.board = [[0 for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]

        self.board_sprite_list = arcade.SpriteList()

        texture_list = []
        for color in COLORS:
            image = Image.new('RGBA', (WIDTH, HEIGHT), color)
            texture_list.append((arcade.Texture(str(color), image=image)))

        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()

                for texture in texture_list:
                    sprite.append_texture(texture)

                sprite.set_texture(0)
                sprite.center_x = (CELL_MARGIN + WIDTH) * column + BORDER_MARGIN + WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - (CELL_MARGIN + HEIGHT) * row + BORDER_MARGIN + HEIGHT // 2

                self.board_sprite_list.append(sprite)

        self.update_board()

    def update_board(self):
        """
        Update the sprite list to reflect the contents of the 2d grid
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * COLUMN_COUNT + column
                self.board_sprite_list[i].set_texture(v)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        self.clear()
        self.board_sprite_list.draw()
        self.draw_snake()

    def on_update(self, dt):
        self.frame_count += 1
        if self.frame_count % SPEED == 0:
            self.drop()

    def draw_snake(self):
        for i in range(len(self.snake.coordinates)):
            offset_y, offset_x = self.snake.coordinates[i]
            color = COLORS[self.snake.colors[i]]

            # Do the math to figure out where the box is
            x = (CELL_MARGIN + WIDTH) * offset_x + BORDER_MARGIN + WIDTH // 2
            y = SCREEN_HEIGHT - (CELL_MARGIN + HEIGHT) * offset_y + BORDER_MARGIN + HEIGHT // 2

            print(f"x={x}, y={y}, color={color}")

            # Draw the box
            arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def drop(self):
        if not self.game_over and not self.paused:
            self.snake.move()
            self.update_board()


def main():
    """ Create the game window, setup, run """
    my_game = MySnake(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
