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
MAIN_BOARD_WIDTH = (WIDTH + CELL_MARGIN) * COLUMN_COUNT
SCORE_BOARD_WIDTH = (WIDTH + CELL_MARGIN) * 4 - CELL_MARGIN
SCREEN_WIDTH = BORDER_MARGIN + MAIN_BOARD_WIDTH + BORDER_MARGIN + SCORE_BOARD_WIDTH + BORDER_MARGIN
SCREEN_HEIGHT = BORDER_MARGIN + (HEIGHT + CELL_MARGIN) * ROW_COUNT - CELL_MARGIN + BORDER_MARGIN
SCREEN_TITLE = "SNAKE"

# Speed of the snake
SPEED = 10

# score for a dot
SCORE_DOT = 10

COLORS = [
    (0,   0,   0, 255),  # black
    (255, 0,   0, 255),  # red
    (0,   150, 0, 255),  # green
    (0,   0,   255, 255),  # blue
    (255, 120, 0, 255),  # orange
    (255, 255, 0, 255),  # yellow
    (180, 0,   255, 255),  # purple
    (0,   220, 220, 255)  # light blue
]


RIGHT = "RIGHT"
LEFT = "LEFT"
UP = "UP"
DOWN = "DOWN"

ALLOWED_DIRECTIONS = {
    RIGHT: [UP, DOWN],
    LEFT: [UP, DOWN],
    UP: [LEFT, RIGHT],
    DOWN: [LEFT, RIGHT]
}

DIRECTIONS = {
    RIGHT: (0, 1),
    LEFT: (0, -1),
    UP: (-1, 0),
    DOWN: (1, 0)
}


def convert_time_to_string(time_in_sec):
    minutes = time_in_sec // 60
    seconds = time_in_sec % 60
    hours = minutes // 60
    minutes = minutes % 60

    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))


class Snake(object):
    def __init__(self):
        self.coordinates = [(0, 2), (0, 1), (0, 0)]
        self.colors = [random.randint(1, 7) for i in range(3)]

    def move(self, y, x):
        self.coordinates.pop()

        head = self.coordinates[0]
        self.coordinates.insert(0, (head[0] + y, head[1] + x))

    def eat(self, dot):
        self.coordinates.append(dot.coordinate)
        self.colors.append(dot.color)


class Dot(object):
    def __init__(self):
        self.coordinate = None
        self.color = None

        self.refresh()

    def refresh(self):
        self.coordinate = (random.randint(0, ROW_COUNT - 1), random.randint(0, COLUMN_COUNT - 1))
        self.color = random.randint(1, 7)


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
        self.direction = RIGHT
        self.dot = None
        self.score = 0
        self.last_time_lapsed = 0
        self.start_time = time.time()

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
                sprite.center_y = SCREEN_HEIGHT - (CELL_MARGIN + HEIGHT) * (row + 1) - BORDER_MARGIN + HEIGHT // 2

                self.board_sprite_list.append(sprite)

        self.update_board()
        self.dot = Dot()

    def reset(self):
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.snake = Snake()
        self.direction = RIGHT
        self.score = 0
        self.last_time_lapsed = 0
        self.start_time = time.time()

        self.board = [[0 for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]

        self.update_board()
        self.dot = Dot()

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
        self.draw_dot()
        self.draw_score()
        self.draw_time()
        self.draw_pause()
        self.draw_help()

    def on_update(self, dt):
        self.frame_count += 1

        if self.frame_count % SPEED == 0:
            self.move()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if LEFT in ALLOWED_DIRECTIONS[self.direction]:
                self.direction = LEFT
        elif key == arcade.key.RIGHT:
            if RIGHT in ALLOWED_DIRECTIONS[self.direction]:
                self.direction = RIGHT
        elif key == arcade.key.UP:
            if UP in ALLOWED_DIRECTIONS[self.direction]:
                self.direction = UP
        elif key == arcade.key.DOWN:
            if DOWN in ALLOWED_DIRECTIONS[self.direction]:
                self.direction = DOWN
        elif key == arcade.key.ESCAPE:
            self.pause()

    def draw_snake(self):
        for i in range(len(self.snake.coordinates)):
            offset_y, offset_x = self.snake.coordinates[i]
            color = COLORS[self.snake.colors[i]]

            x = (CELL_MARGIN + WIDTH) * offset_x + BORDER_MARGIN + WIDTH // 2
            y = SCREEN_HEIGHT - (CELL_MARGIN + HEIGHT) * (offset_y + 1) - BORDER_MARGIN + HEIGHT // 2

            arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def draw_dot(self):
        offset_y, offset_x = self.dot.coordinate

        x = (CELL_MARGIN + WIDTH) * offset_x + BORDER_MARGIN + WIDTH // 2
        y = SCREEN_HEIGHT - (CELL_MARGIN + HEIGHT) * (offset_y + 1) - BORDER_MARGIN + HEIGHT // 2

        arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, COLORS[self.dot.color])

    def draw_score(self):
        width = 4 * (CELL_MARGIN + WIDTH) - BORDER_MARGIN

        x = MAIN_BOARD_WIDTH + BORDER_MARGIN
        y = SCREEN_HEIGHT - 2 * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("SCORE", x, y, arcade.color.WHITE, 20, width=width)

        y = SCREEN_HEIGHT - 3 * (CELL_MARGIN + HEIGHT)
        arcade.draw_text(self.score, x, y, arcade.color.WHITE, 20, width=width, align="right")

    def draw_time(self):
        width = 4 * (CELL_MARGIN + WIDTH) - BORDER_MARGIN

        x = MAIN_BOARD_WIDTH + BORDER_MARGIN
        y = SCREEN_HEIGHT - 5 * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("TIME", x, y, arcade.color.WHITE, 20, width=width)

        y = SCREEN_HEIGHT - 6 * (CELL_MARGIN + HEIGHT)

        if self.paused or self.game_over:
            time_lapsed = self.last_time_lapsed
        else:
            time_lapsed = time.time() - self.start_time + self.last_time_lapsed

        arcade.draw_text(
            convert_time_to_string(time_lapsed), x, y, arcade.color.WHITE, 20, width=width, align="right")

    def draw_pause(self):
        width = 4 * (CELL_MARGIN + WIDTH) - BORDER_MARGIN
        x = MAIN_BOARD_WIDTH + BORDER_MARGIN
        y = SCREEN_HEIGHT - 8 * (CELL_MARGIN + HEIGHT)

        if self.paused:
            current_time = int(time.time())
            if current_time % 2 == 0:
                arcade.draw_text("PAUSED", x, y, arcade.color.RED, 20, width=width, align="center")

        if self.game_over:
            arcade.draw_text("GAME OVER", x, y, arcade.color.RED, 20, width=width, align="center")

    def draw_help(self):
        width = 4 * (CELL_MARGIN + WIDTH) - BORDER_MARGIN
        x = MAIN_BOARD_WIDTH + BORDER_MARGIN

        label_font_size = 15
        text_font_size = 13
        row = 10
        label_color = arcade.color.GREEN

        y = SCREEN_HEIGHT - row * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("UP:", x, y, label_color, label_font_size, width=width)
        y = SCREEN_HEIGHT - (row + 1) * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("MOVE UP", x, y, arcade.color.WHITE, text_font_size, width=width, align="right")

        row += 2
        y = SCREEN_HEIGHT - row * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("LEFT:", x, y, label_color, label_font_size, width=width)
        y = SCREEN_HEIGHT - (row + 1) * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("MOVE LEFT", x, y, arcade.color.WHITE, text_font_size, width=width, align="right")

        row += 2
        y = SCREEN_HEIGHT - row * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("RIGHT:", x, y, label_color, label_font_size, width=width)
        y = SCREEN_HEIGHT - (row + 1) * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("MOVE RIGHT", x, y, arcade.color.WHITE, text_font_size, width=width, align="right")

        row += 2
        y = SCREEN_HEIGHT - row * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("DOWN:", x, y, label_color, label_font_size, width=width)
        y = SCREEN_HEIGHT - (row + 1) * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("MOVE DOWN", x, y, arcade.color.WHITE, text_font_size, width=width, align="right")

        row += 2
        y = SCREEN_HEIGHT - row * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("ESC:", x, y, label_color, label_font_size, width=width)
        y = SCREEN_HEIGHT - (row + 1) * (CELL_MARGIN + HEIGHT)
        arcade.draw_text("PAUSE/RESET", x, y, arcade.color.WHITE, text_font_size, width=width, align="right")

    def move(self):
        if not self.game_over and not self.paused:
            y, x = DIRECTIONS[self.direction]

            if self.check_collision(y, x):
                self.last_time_lapsed += time.time() - self.start_time
                self.game_over = True

            if not self.game_over:
                self.snake.move(y, x)
                self.update_board()

    def check_collision(self, y, x):
        head = self.snake.coordinates[0]
        new_head = (head[0] + y, head[1] + x)

        if new_head in self.snake.coordinates:
            self.game_over = True

        if new_head[0] < 0 or new_head[0] > ROW_COUNT - 1:
            self.game_over = True

        if new_head[1] < 0 or new_head[1] > COLUMN_COUNT - 1:
            self.game_over = True

        if new_head == self.dot.coordinate:
            self.snake.eat(self.dot)
            self.score += SCORE_DOT
            self.dot.refresh()

        return False

    def generate_dot(self):
        while True:
            dot = (random.randint(0, ROW_COUNT - 1), random.randint(0, COLUMN_COUNT - 1))

            if dot not in self.snake.coordinates:
                break

        self.dot = dot

    def pause(self):
        if self.game_over:
            self.reset()
        else:
            if self.paused:
                self.start_time = time.time()
                # self.player = self.sound.play(volume=0.5, loop=True)
                self.paused = False
            else:
                self.last_time_lapsed += time.time() - self.start_time
                # self.sound.stop(self.player)
                self.paused = True


def main():
    """ Create the game window, setup, run """
    my_game = MySnake(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
