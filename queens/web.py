import random
from flask import Flask, render_template_string, request, redirect, url_for
from queens import Queens

app = Flask(__name__)
# 1, 0,3,2

@app.route('/', methods=['GET', 'POST'])
def index():
    n = request.args.get('n', 8, type=int) 

    if request.method == 'POST':
        user_board_str = request.form.get('user_board')
        print(user_board_str)
        try:
            user_board = [int(x) for x in user_board_str.split(',') if x.strip()]
            print(f"user board {user_board}")
            print(f"n is {n}")
        except ValueError:
            pass        # Ensure the user_board has 'n' elements
        if len(user_board) != n:
             return render_template_string(
                """
                <p>an error occurred with board submission. Please try again.</p>
                <a href="{{ url_for('index', n=n) }}">Try again</a>
                """,
                n=n
            )

        # validate user submitted sol
        temp_solver = Queens(n)
        temp_solver.board = user_board 

        is_correct = True
        
        if -1 in temp_solver.board:
             is_correct = False
        else:
            for col in range(n):
                if temp_solver.has_collision(temp_solver.board, col):
                    is_correct = False
                    break
        
        if is_correct:
            solver = Queens(n)
            all_possible_solutions = solver.solve(100000) 
            
            if tuple(user_board) in [tuple(sol) for sol in all_possible_solutions]:
                message = "Congratulations! Your solution is correct!"
                queens_solver = Queens(n)
                html_board = queens_solver.html(user_board)
                return render_template_string(
                    """
                    <h2>{{ message }}</h2>
                    {{ html_board|safe }}
                    <p><a href="{{ url_for('index', n=n) }}">Play again with N={{ n }}</a></p>
                    <p>Enter a different N: <form action="/" method="GET"><input type="number" name="n" value="{{ n }}" min="4"><input type="submit" value="Change N"></form></p>
                    """,
                    message=message, html_board=html_board, n=n
                )
            else:
                message = "Your placement doesn't have collisions but it's not a valid N-Queens solution."
                return render_template_string(
                    """
                    <p>{{ message }}</p>
                    <a href="{{ url_for('index', n=n) }}">Try again</a>
                    """,
                    message=message, n=n
                )

        else:
            message = "Oops! Your solution is incorrect or incomplete. Try again!"
            return render_template_string(
                """
                <p>{{ message }}</p>
                <a href="{{ url_for('index', n=n) }}">Try again</a>
                """,
                message=message, n=n
            )

    else: 
        queens_solver = Queens(n)
        
        all_solutions = queens_solver.solve()
        if not all_solutions:
            return f"No solutions found for N={n}. Please try a different N value."
        
        display_solution_for_colors = random.choice(all_solutions)
        queens_solver.generate_color_regions(display_solution_for_colors)
        
        initial_user_board = [-1] * n

        css = []
        for r in range(n):
            for c in range(n):
                color = queens_solver.colored_board[r][c]
                css.append(f"#{queens_solver.get_cell_id(r, c)} {{ background-color: rgb({color[0]}, {color[1]}, {color[2]}); }}")

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
                cursor: pointer; /* Indicate clickable cells */
                font-size: 2em; /* Make queen symbol larger */
            }}
            {"".join(css)}
        </style>
        """

        html_table_content = f"""
        <div style="text-align: center; margin: 20px;">
            <h1>N-Queens Game (N={n})</h1>
            <p>Click on a square to place or remove a queen. Place {n} queens such that no two queens attack each other.</p>
            <p>The colored regions show where the queens *should* be in a valid solution, but you need to figure out the exact positions!</p>
            <table id="n-queens-board-{n}">
                <tbody>
        """

        for r in range(n):
            html_table_content += "<tr>"
            for c in range(n):
                html_table_content += f"""
                        <td id="{queens_solver.get_cell_id(r, c)}" data-row="{r}" data-col="{c}">
                            </td>
                """
            html_table_content += "</tr>"

        html_table_content += """
                </tbody>
            </table>
            <form id="game-form" action="/" method="POST" style="margin-top: 20px;">
                <input type="hidden" name="user_board" id="user-board-input" value="">
                <input type="hidden" name="n" value="{{ n }}">
                <button type="submit">Check Solution</button>
            </form>
            <p>Current N: {{ n }}</p>
            <p>Enter a different N: <form action="/" method="GET"><input type="number" name="n" value="{{ n }}" min="4"><input type="submit" value="Change N"></form></p>
        </div>
        """
        
        js_script = f"""
        <script>
            const N = {n};
            let userBoard = {initial_user_board}; 
            const cells = document.querySelectorAll('td');
            const userBoardInput = document.getElementById('user-board-input');

            function updateBoard() {{
                cells.forEach(cell => {{
                    const row = parseInt(cell.dataset.row);
                    const col = parseInt(cell.dataset.col);
                    if (userBoard[col] === row) {{
                        cell.innerHTML = '&#9813;'; // Queen symbol
                    }} else {{
                        cell.innerHTML = '';
                    }}
                }});
                userBoardInput.value = userBoard.join(',');
            }}

            cells.forEach(cell => {{
                cell.addEventListener('click', function() {{
                    const row = parseInt(this.dataset.row);
                    const col = parseInt(this.dataset.col);

                    if (userBoard[col] === row) {{
                        // Queen is already here, remove it
                        userBoard[col] = -1;
                    }} else {{
                        // Place queen here
                        userBoard[col] = row;
                    }}
                    updateBoard();
                }});
            }});

            updateBoard();
        </script>
        """

        return render_template_string(
            """
            <head>
                <title>N-Queens Game</title>
                {{ html_board_style|safe }}
            </head>
            <body>
                {{ html_board_content|safe }}
                {{ js_script|safe }}
            </body>
            </html>
            """,
            html_board_style=style,
            html_board_content=html_table_content,
            js_script=js_script,
            n=n
        )

if __name__ == '__main__':
    app.run(debug=True)
