

# Global variables
n =0
num_sets = 0
trail = None
players = ['X', 'O']
scores = {'X': 0, 'O': 0}  # Record points each player
wins = {'X': 0, 'O': 0}    # Number of wins each player
grid = []
#move_history = []  # Store moves (though unused)

# Input validation
while True:
    try:
        n = int(input("Enter grid size (odd number and >= 3, e.g 3, 5, 7):"))
        if n < 3 or n % 2 == 0:
            print("Grid size must be greater than 3 and odd number.")
            continue
        break
    except ValueError:
        print("Invalid input! Must be integer.")

while True:
    try:
        num_sets = int(input("Enter number of sets to play (at least 1): "))
        if num_sets < 1:
            print("Number of sets must be at least 1.")
            continue
        break
    except ValueError:
        print("Invalid input! Must be integer.")

while True:
    try:
        trail = int(input(f"Enter number of consecutive symbols to win (3 to {n}): "))
        if trail < 3:
            print("Number must be greater than or equal to 3.")
            continue
        if trail > n:
            print(f"Number must be less than or equal to {n} (grid size).")
            continue
        break
    except ValueError:
        print("Invalid input! Must be integer.")

# Define grid and display functions
def create_grid(n: int) -> list[list[str]]:
    grid = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(' ')
        grid.append(row)
    return grid

def display_grid(grid: list[list[str]]):
    # Print column labels (1 to n)
    print("   ", end="")
    for col in range(1, n + 1):
        print(f" {col}  ", end="")
    print()

    # Print rows with row labels (1 to n)
    for row in range(n):
        print(f"{row + 1:2} ", end="")  # Row label starting from 1
        row_ele = '|'
        for cell in grid[row]:
            row_ele += f" {cell} |"
        print(row_ele)

# Define game logic functions
def is_valid_move(row, col):
    # Adjust for 0-based internal grid
    row = row - 1
    col = col - 1
    if row < 0 or row >= n or col < 0 or col >= n:
        return False
    if grid[row][col] != ' ':
        return False
    return True

def check_win(player):
    for row in range(n):
        for col in range(n - trail + 1):
            if all(grid[row][col + i] == player for i in range(trail)):
                return True
    for col in range(n):
        for row in range(n - trail + 1):
            if all(grid[row + i][col] == player for i in range(trail)):
                return True
    for row in range(n - trail + 1):
        for col in range(n - trail + 1):
            if all(grid[row + i][col + i] == player for i in range(trail)):
                return True
    for row in range(n - trail + 1):
        for col in range(trail - 1, n):
            if all(grid[row + i][col - i] == player for i in range(trail)):
                return True
    return False

def is_grid_full():
    for row in range(n):
        for col in range(n):
            if grid[row][col] == ' ':
                return False
    return True

def calculate_score():
    empty_cells = 0
    for row in range(n):
        for col in range(n):
            if grid[row][col] == ' ':
                empty_cells += 1
    return empty_cells

# Main game function
def play_game():
    global scores, wins, grid
    game_number = 1

    while game_number <= num_sets:
        print("=== Set", game_number, "of", num_sets, "===")
        grid = create_grid(n)
        current_player = 0  # 0 for X, 1 for O
        game_over = False

        while not game_over:
            player = players[current_player]
            print("Player", player, "turn (Set Scores: X =", scores['X'], ", O =", scores['O'], ")")

            move = input("Enter row,col (e.g., 1,1) or 'q' to quit: ").lower()

            if move == 'q':
                print("Game over. Final set scores: X =", scores['X'], ", O =", scores['O'])
                print("Sets won: X =", wins['X'], ", O =", wins['O'])
                return

            try:
                row, col = map(int, move.split(','))
                # Validate input range before adjusting
                if row < 1 or row > n or col < 1 or col > n:
                    print(f"Coordinates must be between 1 and {n}.")
                    continue
            except (ValueError, IndexError):
                print("Invalid input! Use format 'row,col' (e.g., 1,1).")
                continue

            if not is_valid_move(row, col):
                print("Invalid move! Cell is occupied or out of bounds.")
                continue

            # Adjust for 0-based internal grid
            grid[row - 1][col - 1] = player
            display_grid(grid)  # Update and display grid after each move

            if check_win(player):
                score = calculate_score()
                scores[player] += score
                wins[player] += 1
                print("Player", player, "wins this set! Gained", score, "points!")
                print("Set Scores: X =", scores['X'], ", O =", scores['O'])
                print("Sets won: X =", wins['X'], ", O =", wins['O'])
                game_over = True
            elif is_grid_full():
                print("This set is a draw!")
                game_over = True

            current_player = (current_player + 1) % 2

        game_number += 1

    print("\n=== Final Results ===")
    print("Sets won: X =", wins['X'], ", O =", wins['O'])
    print("Total points: X =", scores['X'], ", O =", scores['O'])

    if wins['X'] > wins['O']:
        print("Overall winner: Player X!")
    elif wins['O'] > wins['X']:
        print("Overall winner: Player O!")
    else:
        if scores['X'] > scores['O']:
            print("Tie in sets! Player X wins by points!")
        elif scores['O'] > scores['X']:
            print("Tie in sets! Player O wins by points!")
        else:
            print("It's a complete tie!")

# Run the game
print("Welcome to Dynamic Tic-Tac-Toe (n x n Grid)!")
print("Enter 'q' to quit.")
play_game()