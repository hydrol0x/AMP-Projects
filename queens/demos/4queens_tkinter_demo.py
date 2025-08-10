import tkinter as tk
import copy

def noCollisions(board, column, row):
    """Determines whether a board has Queens which attack the same squares
        on a 4x4 chess board.

      Args:
        board (list): A list lists representing the placement of Queens
        column (int): The current column being considered
        row (int):  The current row being considered

      Returns:
        bool: True if there are no collisions, False if there is 1 or more collisions
    """
    n = 4
    #Column Check: Not needed because of how we generate queens

    #Row Check: No 2 queens on the same row
    for j in range(column):
        if board[row][j] == 1:
            return False

    k = 1   #Diagonal Check: /
    while row - k >= 0 and column - k >= 0:
        if board[row - k][column - k] == 1:
            return False
        k += 1

    k = 1  #Diagonal Check: \
    while row + k < n and column - k >= 0:
        if board[row + k][column - k] == 1:
            return False
        k += 1

    return True

def FourQueens():
    """Uses backtracking to identify all solutions to the 4-Queens problem.

     Returns:
       list: A list of all board lists which are solutions to the 4-Queens problem.
   """
    n=4
    #Initialize the board to be empty (0), with no Queens (1)
    board = [ [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0] ]
    solutions = []
    #Place a queen on successive rows, one column at a time
    #beginning with leftmost column
    for r0 in range(n):
        board[r0][0] = 1
        for r1 in range(n):
            board[r1][1] = 1
            if noCollisions(board, 1, r1):
                for r2 in range(n):
                    board[r2][2] = 1
                    if noCollisions(board, 2, r2):
                        for r3 in range(n):
                            board[r3][3] = 1
                            if noCollisions(board, 3, r3):
                                print("board", board)
                                solutions.append(copy.deepcopy(board))
                                print("list",solutions)
                            board[r3][3] = 0
                    board[r2][2] = 0
            board[r1][1] = 0
        board[r0][0] = 0
    print('final list', solutions)
    return solutions

def prettyPrint(board):
    """Draws the board using the tkinter graphics library.
       Columns are labeled with letters (A, B, C, D).
       Rows are labeled with numbers (0, 1, 2, 3).

    """
    appWidth = 450
    appHeight = 450

    app = tk.Tk()
    app.title("Tkinter Python Graphics demo")
    app.geometry(f"{appWidth}x{appHeight}")
    canvas = tk.Canvas(app, bg="#cccccc", width=appWidth-50, height=appHeight-50)
    canvas.pack()

    global logo #make global b/c Pytho garbage collection
                    #https://stackoverflow.com/questions/16424091/why-does-tkinter-image-not-show-up-if-created-in-a-function/63599265#63599265
    logo = tk.PhotoImage(file='queen.png')
    black = True
    for y in range(4):
        black = not black
        for x in range(4):
            if black:
                fc='black'
            else:
                fc="white"
            black = not black
            canvas.create_rectangle(x*100,y*100,(x+1)*100,(y+1)*100, fill=fc, outline='black')
            if board[x][y]==1:
                canvas.create_image(50+x*100, 50+y*100, image=logo, anchor=tk.CENTER)

    app.mainloop()

if __name__ == "__main__":
   print(FourQueens())
   solutions = FourQueens()
   print(f"There are {len(solutions)} solutions to the 4-Queens problem")
   print(solutions[0])
   prettyPrint(solutions[0])
