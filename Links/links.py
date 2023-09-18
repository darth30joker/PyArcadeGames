import random

import arcade
import PIL

ROWS = 24
COLUMNS = 10

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 30

CELL_MARGIN = 3

SCREEN_WIDTH = CELL_MARGIN + (COLUMNS - 1) * (BLOCK_WIDTH + CELL_MARGIN)
SCREEN_HEIGHT = CELL_MARGIN + (ROWS - 1) * (BLOCK_WIDTH + CELL_MARGIN)

COLORS = [
    (0,   0,   0,   255),  # black
    (255, 0,   0,   255),  # red
    (0,   150, 0,   255),  # green
    (0,   0,   255, 255),  # blue
    (255, 120, 0,   255),  # orange
    (255, 255, 0,   255),  # yellow
    (180, 0,   255, 255),  # purple
]

SPEED = 10


def check_collision(board, block, block_x, block_y):
    """
    Test collision with next row
    """
    for cy, row in enumerate(block):
        for cx, cell in enumerate(row):
            if not cell:
                return False
            if block_y + cy == ROWS - 1:
                return True
            if board[cy + block_y][cx + block_x] or board[cy + block_y + 1][cx + block_x]:
                return True

    return False


def join_matrix(matrix, block, block_x, block_y):
    for cy, row in enumerate(block):
        for cx, val in enumerate(row):
            matrix[cy + block_y][cx + block_x] = val

            if cy + block_y == len(matrix) - 1:
                continue

            y = cy + block_y
            while y < len(matrix) - 1:
                if matrix[y + 1][cx + block_x] == 0:
                    matrix[y][cx + block_x], matrix[y + 1][cx + block_x] = matrix[y + 1][cx + block_x], matrix[y][cx + block_x]

                y += 1


def rotate(shape):
    if len(shape) == 1:
        return [[i] for i in shape[0][::-1]]
    if len(shape) == 3:
        return [[i[0] for i in shape]]


def sort_duplicates(duplicates):
    if not duplicates:
        return []

    length = len(duplicates)

    for i in range(length):
        for j in range(length - i - 1):
            if duplicates[j][0] > duplicates[j + 1][0]:
                duplicates[j], duplicates[j + 1] = duplicates[j + 1], duplicates[j]

            if duplicates[j][0] == duplicates[j + 1][0] and duplicates[j][1] > duplicates[j + 1][1]:
                duplicates[j], duplicates[j + 1] = duplicates[j + 1], duplicates[j]

    return duplicates


def find_duplicates(board):
    length = len(board[0])
    depth = len(board)
    duplicates = []

    for cy, row in enumerate(board):
        for cx, val in enumerate(row):
            if val > 0:
                # check horizontal
                stack = [(cy, cx)]
                coordinates = [(cy, cx)]
                times = 0
                while stack:
                    times += 1
                    y, x = stack.pop()
                    if x > 0 and board[y][x - 1] == val and (y, x - 1) not in coordinates:
                        stack.append((y, x - 1))
                        coordinates.append((y, x - 1))
                    if x < length - 1 and board[y][x + 1] == val and (y, x + 1) not in coordinates:
                        stack.append((y, x + 1))
                        coordinates.append((y, x + 1))

                if times >= 3:
                    for coordinate in coordinates:
                        if coordinate not in duplicates:
                            duplicates.append(coordinate)

                # check vertical
                stack = [(cy, cx)]
                coordinates = [(cy, cx)]
                times = 0
                while stack:
                    times += 1
                    y, x = stack.pop()
                    if y > 0 and board[y - 1][x] == val and (y - 1, x) not in coordinates:
                        stack.append((y - 1, x))
                        coordinates.append((y - 1, x))
                    if y < depth - 1 and board[y + 1][x] == val and (y + 1, x) not in coordinates:
                        stack.append((y + 1, x))
                        coordinates.append((y + 1, x))

                if times >= 3:
                    for coordinate in coordinates:
                        if coordinate not in duplicates:
                            duplicates.append(coordinate)

    return sort_duplicates(duplicates)


def remove_duplicates(board, duplicates):
    for duplicate in duplicates:
        y, x = duplicate
        board[y][x] = 0

        if y == 0:
            continue

        offset_y = y
        while True:
            if y >= len(board) or offset_y == 0:
                break

            if board[offset_y - 1][x] == 0:
                break

            board[offset_y - 1][x], board[offset_y][x] = board[offset_y][x], board[offset_y - 1][x]

            offset_y -= 1

    return board


class MyLinks(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.board = None
        self.board_sprite_list = None
        self.frame_count = 0
        self.game_over = False

        self.block = None
        self.block_x = 0
        self.block_y = 1

    def setup(self):
        self.board = [[0 for j in range(COLUMNS)] for i in range(ROWS)]

        self.board_sprite_list = arcade.SpriteList()

        new_textures = []
        for color in COLORS:
            # noinspection PyUnresolvedReferences
            image = PIL.Image.new('RGBA', (BLOCK_WIDTH, BLOCK_HEIGHT), color)
            new_textures.append(arcade.Texture(str(color), image=image))

        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()

                for texture in new_textures:
                    sprite.append_texture(texture)

                sprite.set_texture(0)
                sprite.center_x = (CELL_MARGIN + BLOCK_WIDTH) * column + CELL_MARGIN + BLOCK_WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - (CELL_MARGIN + BLOCK_HEIGHT) * row + BLOCK_HEIGHT // 2

                self.board_sprite_list.append(sprite)

        self.update_board()
        self.generate_new_block()

    def on_draw(self):
        self.clear()
        self.board_sprite_list.draw()
        self.draw_block(self.block, self.block_x, self.block_y)

    def on_update(self, dt):
        self.frame_count += 1
        if self.frame_count % SPEED == 0:
            self.drop()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.UP:
            self.rotate_stone()
        elif key == arcade.key.DOWN:
            self.drop()

    def update_board(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * COLUMNS + column
                self.board_sprite_list[i].set_texture(v)

    def generate_new_block(self):
        if not self.game_over:
            self.block = [[random.randint(1, 4) for i in range(3)]]
            self.block_x = 4
            self.block_y = 0

            if check_collision(self.board, self.block, self.block_x, self.block_y):
                self.game_over = True

    def draw_block(self, grid, offset_x, offset_y):
        """
        Draw the grid. Used to draw the falling stones. The board is drawn
        by the sprite list.
        """
        # Draw the grid
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                if grid[row][column]:
                    color = COLORS[grid[row][column]]
                    # Do the math to figure out where the box is
                    x = (CELL_MARGIN + BLOCK_WIDTH) * (column + offset_x) + CELL_MARGIN + BLOCK_WIDTH // 2
                    y = SCREEN_HEIGHT - (CELL_MARGIN + BLOCK_HEIGHT) * (row + offset_y) + BLOCK_HEIGHT // 2

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, color)

    def drop(self):
        if not self.game_over:
            self.block_y += 1

            if check_collision(self.board, self.block, self.block_x, self.block_y):
                join_matrix(self.board, self.block, self.block_x, self.block_y)

                duplicates = find_duplicates(self.board)

                print(f"duplicates: {duplicates}")

                if duplicates:
                    self.board = remove_duplicates(self.board, duplicates)

                self.update_board()
                self.generate_new_block()

    def move(self, offset):
        if not self.game_over:
            x = self.block_x + offset

            if x < 0:
                x = 0

            if x > COLUMNS - len(self.block[0]) - 1:
                x = COLUMNS - len(self.block[0]) - 1

            if not check_collision(self.board, self.block, x, self.block_y):
                self.block_x = x

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over:
            new_block = rotate(self.block)

            if self.block_x + len(new_block[0]) >= COLUMNS:
                self.block_x = COLUMNS - len(new_block[0])

            self.block = new_block


def main():
    """ Create the game window, setup, run """
    my_game = MyLinks(SCREEN_WIDTH, SCREEN_HEIGHT, "MyLinks")
    my_game.setup()
    arcade.run()


if __name__ == "__main__":
    main()