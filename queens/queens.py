import random
import collections
Board = list[int] 
rgb = tuple[int,int,int]

class Queens:
    def __init__(self, n:int):
        self.n: int = n
        self.board: Board = [] # list representing row position of queen according to col index
        self.initialize_empty_board()
        self.all_solutions: list[Board] = []
        # self.colors: list[dict] = []
        self.queen_colors: dict[int, rgb] = {}
        self.region_grid: list[list[int | None]] = []
        self.colored_board: list[list[rgb]] = []


    def get_random_color(self)->rgb:
        r = random.randint(50, 200) 
        g = random.randint(50, 200)
        b = random.randint(50, 200)

        return (r,g,b )

    def generate_color_regions(self, board: Board):
        """For a given board with a solved n queens layout, generate and store n colored randomly regions surrounding each queen."""
        self.queen_colors = {}
        self.region_grid = [[None for _ in range(self.n)] for _ in range(self.n)]
        self.colored_board = [[(0, 0, 0) for _ in range(self.n)] for _ in range(self.n)]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # use bfs to fill
        que = collections.deque()

        for col, row in enumerate(board):
            color = self.get_random_color()
            queen = col
            self.queen_colors[queen] = color

            que.append((row, col, queen))
            self.region_grid[row][col] = queen 

        while que:
            curr_row, curr_col, curr_queen = que.popleft()

            neighbors = []
            for drow,dcol in directions:
                new_row = drow + curr_row
                new_col = dcol + curr_col

                if 0 <= new_row < self.n and 0 <= new_col < self.n:
                    if self.region_grid[new_row][new_col] is None:
                        neighbors.append((new_row, new_col))

            random.shuffle(neighbors)

            for new_row, new_col in neighbors:
                if self.region_grid[new_row][new_col] is None:
                    self.region_grid[new_row][new_col] = curr_queen
                    que.append((new_row, new_col, curr_queen))

            for row in range(self.n):
                for col in range(self.n):
                    cell_queen = self.region_grid[row][col]
                    if cell_queen is not None:
                        self.colored_board[row][col] = self.queen_colors[cell_queen]




    def initialize_empty_board(self):
        '''Sets all board positions to -1'''
        self.board = [-1]*self.n

    def has_collision(self, board: list[int], current_col:int)->bool:
        '''Considers columns to the left of the current column to check for row and diagonal conflicts in the board.
            Assumes all columns to the left of the current column have a non-negative integer ie a Queen has been placed

            Args:
                board (list): Non-negative entries indicate a particular row for the column represented by the index of the list
                current_col (int): The current column being considered

            Returns:
                bool: True indicates two Queens attack the same square, otherwise False
        
            Examples
            --------
            >>> q = Queens(8)
            >>> q.has_collision([0, 6, 4, 7, 3, -1, -1, -1], 4)
            True

            >>> q = Queens(8)
            >>> q.has_collision([0, 6, 4, 7, 3, 6, -1, -1], 5)
            True

            >>> q = Queens(8)
            >>> q.has_collision([2, 4, 1, 7, 5, 3, 6, 0], 7)
            False
        '''
        
        current_row = board[current_col]

        for col, row in enumerate(board[:current_col]): 
            # print(f"col: {col}; row: {row}, current_col: {current_col}, current_row: {current_row}")
            if row == current_row:
                # print(f"{board} has a Straight collision at {col}. row: {row}; current_row {current_row}")
                return True # Collision on a straight line 

            if abs(current_col - col) == abs(current_row - row):
                # print(f"{board} has a diagonal collision at {current_col}")
                return True # collision on a diagonal
        return False
            

    def validate(self) -> bool:
        pass

    
    def solve(self, num_sol:int=1000) -> list[list[int]]:
        '''Wrapper method for generating requested number of recursive n-queens solutions.
           If num_sol is greater than the total number of solutions, returns all solutions.
            
            Args:
                num_sol (int): The desired number of solutions

            Returns:
                list of 1-D solutions of length n for the n-queens problem 
        '''
        self.initialize_empty_board()
        self.all_solutions=[]
        self.search_all(0, num_sol) #recursive helper 
        return self.all_solutions

    def search_all(self, current_col:int=0, max_sol:int=1000 )->None:
        '''Finds multiple solutions to the n-queens problem. 
           If max_sol is greater than the total number of solutions, returns all solutions.
           Stores all solutions in self.all_solutions

            Args:
                max_sol (int): The desired number of solutions
                current_col (int): The current column being considered

            Returns:
                bool: True/False depending on whether a solution of size board_size has been found
        '''
        # check that we haven't found all requested solutions already
        if len(self.all_solutions) >= max_sol:
            return

        if current_col == self.n:
            # we passed the last column, don't overflow
            self.all_solutions.append(self.board.copy()) # save current state since we found a solution
            return
        for row in range(self.n): # there are always n rows
            self.board[current_col] = row
            if not self.has_collision(self.board, current_col):
                solution = self.search_all(current_col + 1, max_sol)
                if solution:
                    # self.all_solutions.append(self.board)
                    print(self.board) 

    def get_cell_id(self, r: int, c: int) -> str:
        return f"cell-{r}-{c}"

    def html(self, board: Board) -> str:
        self.generate_color_regions(board)

        css = []
        for r in range(self.n):
            for c in range(self.n):
                color = self.colored_board[r][c]
                css.append(f"#{self.get_cell_id(r, c)} {{ background-color: rgb({color[0]}, {color[1]}, {color[2]}); }}")

        style = f"""
        <style>
            table {{
                margin: 0 auto;
            }}
            td {{
                width: 40px; 
                height: 40px; 
                text-align: center;
                vertical-align: middle;
                border: 1px solid gray; 
            }}
            {"".join(css)}
        </style>
        """

        html_table_content = f"""
        <div style="text-align: center; margin: 20px;">
            <h1>Queens Solution</h1>
            <table id="n-queens-board-{self.n}">
                <tbody>
        """

        # table
        for r in range(self.n):
            html_table_content += "<tr>"
            for c in range(self.n):
                is_queen = (board[c] == r)

                html_table_content += f"""
                        <td id="{self.get_cell_id(r, c)}">
                            {'♛' if is_queen else ''}
                        </td>
                """
            html_table_content += "</tr>"

        html_table_content += """
                </tbody>
            </table>
        </div>
        """
        return style + html_table_content



    def prettify(self, board):
        """Represents the board as a string. 
            -Queens are represented with a Q
            -Empty squares are represented with a .
            -The first character in the string is \n, and each line of the board ends with \n

            Args:
            board (list): Non-negative entries indicate a particular row for the column reprented by the index of the list
        
            Returns:
            A list of strings representing a human-readable version of the board
        """
        self.board=board
        pretty_board = [["."]*self.n for i in range(self.n)]
        for col_index, spot in enumerate(self.board): 
            if spot >=0 and spot <=len(self.board):
                pretty_board[spot][col_index]="Q"

        string_version=""
        for row in pretty_board:
            string_row=""
            for square in row:
                string_row+=square
            string_version+=string_row+"\n"
        return string_version[:-1] #remove last \n
    
    def __str__(self) -> list[str]:
        return f"{self.n}-Queens has {len(self.solve(100000))} solutions"


if __name__ == "__main__":
    N =10 
    queens_solver = Queens(N)
    all_solutions = queens_solver.solve()

    if all_solutions:
        random_solution = random.choice(all_solutions)

        html= queens_solver.html(random_solution)
        out = "n_queens_solution.html"

        with open(out, "w") as f:
            f.write(html)
        print(f"HTML saved to {out}")
    else:
        print(f"No solutions found for N={N}.")


