# N-Queens Problem using Backtracking

def is_safe(board, row, col):
    """
    Check if placing a queen at (row, col) is safe.
    board[row] stores the column index of the queen in that row.
    """
    for prev_row in range(row):
        placed_col = board[prev_row]

        # Check same column
        if placed_col == col:
            return False

        # Check diagonals
        if abs(placed_col - col) == abs(prev_row - row):
            return False

    return True


def solve_n_queens_util(board, row, n, solutions):
    """
    Recursive utility to place queens row by row.
    """
    if row == n:
        # Found a valid arrangement
        solutions.append(board.copy())
        return

    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            solve_n_queens_util(board, row + 1, n, solutions)
            # Backtrack (no need to reset board[row] because it will be overwritten)


def solve_n_queens(n):
    """
    Solve the N-Queens problem and return all solutions.
    Each solution is represented as a list of column positions.
    """
    board = [-1] * n  # -1 means no queen placed in that row
    solutions = []
    solve_n_queens_util(board, 0, n, solutions)
    return solutions


def print_solutions(solutions, n):
    """
    Print the board configurations for all solutions.
    """
    for idx, sol in enumerate(solutions, start=1):
        print(f"Solution {idx}:")
        for row in range(n):
            line = ""
            for col in range(n):
                line += "Q " if sol[row] == col else ". "
            print(line)
        print()


if __name__ == "__main__":
    try:
        n = int(input("Enter the number of queens (N): "))
        if n <= 0:
            print("N must be a positive integer.")
        else:
            solutions = solve_n_queens(n)
            print(f"\nTotal solutions for {n}-Queens: {len(solutions)}\n")
            print_solutions(solutions, n)
    except ValueError:
        print("Invalid input. Please enter an integer.")
