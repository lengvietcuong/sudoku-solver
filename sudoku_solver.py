from termcolor import cprint


def show(board, empty_cells=set()):
    i = 0
    for box_row in (0, 3, 6):
        print("—————————————————————————")
        for row in range(box_row, box_row + 3):
            for box_col in (0, 3, 6):
                print("|", end = " ")
                for col in range(box_col, box_col + 3):
                    if i < len(empty_cells) and [row, col] == empty_cells[i]:
                        cprint(board[row][col], "cyan", end = " ")
                        i += 1
                    else:
                        print(board[row][col], end = " ")
            print("|")
    print("—————————————————————————")


def precompute(board):
    """Marks empty cells and already filled nums"""
    empty_cells = []
    rows = [[False] * 9 for _ in range(9)]
    cols = [[False] * 9 for _ in range(9)]
    boxes = [[[False] * 9 for _ in range(3)] for _ in range(3)]

    for row in range(9):
        for col in range(9):
            if board[row][col] == " ":
                empty_cells.append([row, col])
                continue
            num = int(board[row][col])
            # check if num is already present in its row, col, or box
            if (rows[row][num - 1] or
                    cols[col][num - 1] or
                    boxes[row // 3][col // 3][num - 1]):
                raise ValueError("Invalid Input")
            rows[row][num - 1] = True
            cols[col][num - 1] = True
            boxes[row // 3][col // 3][num - 1] = True

    return empty_cells, rows, cols, boxes


def solve(board):
    """Solves in-place, stops when 1 solution is found"""
    empty_cells, rows, cols, boxes = precompute(board)
    
    i, num_empty = 0, len(empty_cells)
    while i < num_empty:
        row, col = empty_cells[i]
        # determine the starting value to test
        if board[row][col] == " ":  # first time at this cell
            start = 1
        else:  # previously tested -> erase previous num
            num = int(board[row][col])
            board[row][col] = " "
            rows[row][num - 1] = False
            cols[col][num - 1] = False
            boxes[row // 3][col // 3][num - 1] = False
            start = num + 1

        for num in range(start, 10):  # test remaining possible nums
            if (rows[row][num - 1] or
                    cols[col][num - 1] or
                    boxes[row // 3][col // 3][num - 1]):  # already present
                continue
            board[row][col] = str(num)
            rows[row][num - 1] = True
            cols[col][num - 1] = True
            boxes[row // 3][col // 3][num - 1] = True
            i += 1
            break
        else:  # no possible nums -> go to previous cell & try a new num
            i -= 1
            if i < 0:
                raise ValueError("No Solution")
    
    show(board, empty_cells)


def find_all_solutions(board, empty_cells=None, rows=None, cols=None, boxes=None, i=0):
    if empty_cells is None:
        empty_cells, rows, cols, boxes = precompute(board)

    if i == len(empty_cells):  # solved
        show(board, empty_cells)
    else:
        row, col = empty_cells[i]
        for num in range(1, 10):  # test remaining possible values
            if (rows[row][num - 1] or
                    cols[col][num - 1] or
                    boxes[row // 3][col // 3][num - 1]):
                continue  # num already present

            board_copy = [[board[row][col] for col in range(9)] for row in range(9)]
            rows_copy = [rows[row].copy() for row in range(9)]
            cols_copy = [cols[col].copy() for col in range(9)]
            boxes_copy = [[boxes[row][col].copy()
                           for col in range(3)] for row in range(3)]

            board_copy[row][col] = str(num)
            rows_copy[row][num - 1] = True
            cols_copy[col][num - 1] = True
            boxes_copy[row // 3][col // 3][num - 1] = True

            find_all_solutions(board_copy, 
                    empty_cells, rows_copy, cols_copy, boxes_copy, i + 1)


cells = input("Enter board in 1 line (empty cells as spaces):\n")
board = [[cells[9*j + i] for i in range(9)] for j in range(9)]

# board = [["5", "3", " ", " ", "7", " ", " ", " ", " "],
#         ["6", " ", " ", "1", "9", "5", " ", " ", " "],
#         [" ", "9", "8", " ", " ", " ", " ", "6", " "],
#         ["8", " ", " ", " ", "6", " ", " ", " ", "3"],
#         ["4", " ", " ", "8", " ", "3", " ", " ", "1"],
#         ["7", " ", " ", " ", "2", " ", " ", " ", "6"],
#         [" ", "6", " ", " ", " ", " ", "2", "8", " "],
#         [" ", " ", " ", "4", "1", "9", " ", " ", "5"],
#         [" ", " ", " ", " ", "8", " ", " ", "7", "9"]]

solve(board)
# find_all_solutions(board)
