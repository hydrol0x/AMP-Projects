def eight_queens_exhaustive():
    '''Example of an exhaustive approach to solving the 8-queens problem'''
    board = [-1] * 8  #no queens in any column
    for i in range(8):
        board[0] = i
        for j in range(8):
            board[1] = j
            if not has_collision(board, 1):
                continue
            for k in range(8):
                board[2] = k
                if not has_collision(board, 2):
                    continue
                for l in range(8):
                    board[3] = l
                    if not has_collision(board, 3):
                        continue
                    for m in range(8):
                        board[4] = m
                        if not has_collision(board, 4):
                            continue
                        for o in range(8):
                            board[5] = o
                            if not has_collision(board, 5):
                                continue
                            for p in range(8):
                                board[6] = p
                                if not has_collision(board, 6):
                                    continue
                                for q in range(8):
                                    board[7] = q
                                    if has_collision(board, 7):
                                        print (board)