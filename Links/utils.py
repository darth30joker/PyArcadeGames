COLUMNS = 10
ROWS = 24

BLOCKS = [
    [[1, 1, 1]],
    [[1], [1], [1]]
]


def new_board(columns, rows):
    return [[0 for i in range(columns)] for j in range(rows)]


def check_collision(board, block, block_x, block_y):
    """
    Test collision with next row
    """
    for cy, row in enumerate(block):
        for cx, cell in enumerate(row):
            # print(f"collision  - cell: {cell}, cx: {cx}, cy: {cy}, block_x: {block_x}, block_y: {block_y}")
            if not cell:
                return False
            if block_y + cy == ROWS - 1 or block_x + cx == 1 or block_x + cx == COLUMNS - 1:
                return True
            if board[cy + block_y][cx + block_x - 1]:
                return True
            if board[cy + block_y][cx + block_x + 1]:
                return True
            if board[cy + block_y + 1][cx + block_x]:
                return True
    return False


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
                times = 1
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
                times = 1
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

    return duplicates


def sort_duplicates(duplicates):
    length = len(duplicates)

    for i in range(length):
        for j in range(length - i - 1):
            if duplicates[j][0] > duplicates[j + 1][0]:
                duplicates[j], duplicates[j + 1] = duplicates[j + 1], duplicates[j]

            if duplicates[j][0] == duplicates[j + 1][0] and duplicates[j][1] > duplicates[j + 1][1]:
                duplicates[j], duplicates[j + 1] = duplicates[j + 1], duplicates[j]

    return duplicates


def remove_duplicates(board, duplicates):
    for duplicate in duplicates:
        y, x = duplicate
        if y > 0 and not board[y - 1][x]:
            continue

        if y > 0 and board[y - 1][x]:
            for offset_y in range(y):
                if board[offset_y + 1][x]:
                    board[offset_y + 1][x] = board[offset_y][x]
                else:
                    break


def test_collision(board, block, block_x, block_y):
    print(f"Tested {block}, x={block_x}, y={block_y}, result={check_collision(board, block, block_x, block_y)}")


def test_check_collision():
    board = new_board(COLUMNS, ROWS)

    print(f"board columns: {len(board[0])}, rows: {len(board)}")

    for block in BLOCKS:
        test_collision(board, block, 3, 20)
        test_collision(board, block, 3, 21)
        test_collision(board, block, 3, 22)
        test_collision(board, block, 3, 23)


def test_find_duplicates():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 2, 2, 2, 0, 5, 5, 5],
        [0, 1, 2, 0, 0, 0, 0, 2, 0, 0],
        [0, 1, 3, 0, 4, 4, 0, 2, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 6, 6, 6, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    duplicates = find_duplicates(board)
    print(duplicates)
    print(sort_duplicates(duplicates))


if __name__ == "__main__":
    test_find_duplicates()
