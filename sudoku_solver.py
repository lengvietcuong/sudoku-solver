def show(board):
    for box_row in (0, 3, 6):
        print("—————————————————————————")
        for row in range(box_row, box_row + 3):
            for box_col in (0, 3, 6):
                print("|", end = " ")
                for col in range(box_col, box_col + 3):
                    if board[row][col]:
                        print(board[row][col], end = " ")
                    else:
                        print(" ", end = " ")
            print('|')
    print("—————————————————————————")


def precompute(board):
    """Gets coordinates of empty cells and marks off filled nums for all rows, cols, and boxes"""
    empty_cells = []
    rows = [[False for _ in range(9)] for _ in range(9)]
    cols = [[False for _ in range(9)] for _ in range(9)]
    boxes = [[[False for _ in range(9)] for _ in range(3)] for _ in range(3)]

    for row in range(9):
        for col in range(9):
            if not board[row][col]:
                empty_cells.append([row, col])
                continue
            num = int(board[row][col])
            # check if num is already present in its row, col, or box
            if rows[row][num - 1] or cols[col][num - 1] or boxes[row // 3][col // 3][num - 1]:
                raise ValueError("Invalid Input")
            rows[row][num - 1] = True
            cols[col][num - 1] = True
            boxes[row // 3][col // 3][num - 1] = True

    return empty_cells, rows, cols, boxes


def solve(board):
    """Solves the board in-place, stops when one solution is found"""
    empty_cells, rows, cols, boxes = precompute(board)
    
    i, num_empty = 0, len(empty_cells)
    while i < num_empty:
        row, col = empty_cells[i]
        # determine the starting value to test
        if not board[row][col]:  # first time at this cell
            start = 1
        else:  # previously tested -> erase previous value and try the next possible number
            num = int(board[row][col])
            board[row][col] = ""
            rows[row][num - 1] = cols[col][num - 1] = boxes[row // 3][col // 3][num - 1] = False
            start = num + 1

        for num in range(start, 10):  # test remaining possible values
            if rows[row][num - 1] or cols[col][num - 1] or boxes[row // 3][col // 3][num - 1]:
                continue  # num already present

            board[row][col] = str(num)
            rows[row][num - 1] = True
            cols[col][num - 1] = True
            boxes[row // 3][col // 3][num - 1] = True
            i += 1
            break
        else:  # no possible value -> return to previously tested cell to try a new number there
            i -= 1
            if i < 0:
                raise ValueError("No Solution")


def find_all_solutions(board, empty_cells=None, rows=None, cols=None, boxes=None, i=0):
    """Generates all poissible solutions as a generator, does not modify the original board"""
    if empty_cells is None:
        empty_cells, rows, cols, boxes = precompute(board)

    if i == len(empty_cells):  # solved
        yield board
    else:
        row, col = empty_cells[i]
        for num in range(1, 10):  # test remaining possible values
            if rows[row][num - 1] or cols[col][num - 1] or boxes[row // 3][col // 3][num - 1]:
                continue  # num already present

            board_copy = [[board[row][col] for col in range(9)] for row in range(9)]
            rows_copy = [rows[row].copy() for row in range(9)]
            cols_copy = [cols[col].copy() for col in range(9)]
            boxes_copy = [[boxes[row][col].copy() for col in range(3)] for row in range(3)]

            board_copy[row][col] = num
            rows_copy[row][num - 1] = True
            cols_copy[col][num - 1] = True
            boxes_copy[row // 3][col // 3][num - 1] = True

            for solution in find_all_solutions(board_copy, 
                    empty_cells, rows_copy, cols_copy, boxes_copy, i + 1):
                yield solution
                

# board_1 has only one solution
board_1 = [["5","3","","","7","","","",""],
         ["6","","","1","9","5","","",""],
         ["","9","8","","","","","6",""],
         ["8","","","","6","","","","3"],
         ["4","","","8","","3","","","1"],
         ["7","","","","2","","","","6"],
         ["","6","","","","","2","8",""],
         ["","","","4","1","9","","","5"],
         ["","","","","8","","","7","9"]]
solve(board_1)
print("Solution of board_1:")
show(board_1)
print("\n")

# board_2 has multiple solutions
board_2 = [["","","","","7","","","",""],
         ["6","","","1","9","5","","",""],
         ["","9","8","","","","","6",""],
         ["8","","","","6","","","","3"],
         ["4","","","8","","3","","","1"],
         ["7","","","","2","","","","6"],
         ["","6","","","","","2","8",""],
         ["","","","4","1","9","","","5"],
         ["","","","","8","","","7","9"]]
print("Solutions of board_2:")
for solution in find_all_solutions(board_2):
    show(solution)
    print("\n")
