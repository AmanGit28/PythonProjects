import tkinter as tk
from tkinter import messagebox
import numpy as np

# Initialize a 9x9 matrix for Sudoku and its corresponding Entry widgets
matrix = np.zeros((9, 9), dtype="int16")  # Represents the Sudoku grid as a 2D array
entry_widgets = [[None for _ in range(9)] for _ in range(9)]  # Stores Entry widget references

# Initialize the main Tkinter window
window = tk.Tk()
window.title("Sudoku Solver")  # Title of the window
window.geometry("720x720")  # Set window dimensions
window.configure(bg="#EAF6FF")  # Set background color


# Function to check the validity of the Sudoku grid
def truevalue(matrix):
    """Validates the current Sudoku grid for duplicate values."""
    # Check each row for duplicates
    for row in range(9):
        seen = set()
        for col in range(9):
            num = matrix[row][col]
            if num != 0:  # Ignore empty cells
                if num in seen:
                    return False  # Duplicate found in the row
                seen.add(num)

    # Check each column for duplicates
    for col in range(9):
        seen = set()
        for row in range(9):
            num = matrix[row][col]
            if num != 0:  # Ignore empty cells
                if num in seen:
                    return False  # Duplicate found in the column
                seen.add(num)

    # Check each 3x3 subgrid for duplicates
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            seen = set()
            for row in range(start_row, start_row + 3):
                for col in range(start_col, start_col + 3):
                    num = matrix[row][col]
                    if num != 0:  # Ignore empty cells
                        if num in seen:
                            return False  # Duplicate found in the subgrid
                        seen.add(num)

    return True  # The grid is valid


# Backtracking function to solve the Sudoku puzzle
def solve_sudoku_logic(matrix):
    """Uses backtracking to solve the Sudoku puzzle."""
    for row in range(9):
        for col in range(9):
            if matrix[row][col] == 0:  # Find an empty cell
                for num in range(1, 10):  # Try numbers 1 to 9
                    matrix[row][col] = num
                    if truevalue(matrix) and solve_sudoku_logic(matrix):
                        return True  # If valid, continue solving
                    matrix[row][col] = 0  # Reset cell if invalid (backtrack)
                return False  # No valid number found, return failure
    return True  # Puzzle is solved


# Function to solve the Sudoku puzzle
def solvesudoku():
    """Retrieves values from the grid, validates the input, and solves the puzzle."""
    # Populate the matrix with values from the Entry widgets
    for row in range(9):
        for col in range(9):
            value = entry_widgets[row][col].get()
            matrix[row][col] = int(value) if value else 0  # Convert empty cells to 0

    # Validate the initial input
    if not truevalue(matrix):
        messagebox.showinfo("Error", "Invalid Sudoku grid. Please fix it.")
        return

    # Attempt to solve the puzzle
    if solve_sudoku_logic(matrix):
        # Update the Entry widgets with the solved grid
        for row in range(9):
            for col in range(9):
                entry_widgets[row][col].delete(0, tk.END)
                entry_widgets[row][col].insert(0, str(matrix[row][col]))
        messagebox.showinfo("Success", "Sudoku solved successfully!")
    else:
        messagebox.showinfo("Error", "No solution exists for the given Sudoku grid.")


# Function to reset the Sudoku grid
def reset_window():
    """Clears the Sudoku grid and resets the matrix."""
    for row in range(9):
        for col in range(9):
            entry_widgets[row][col].delete(0, tk.END)
            matrix[row][col] = 0  # Reset the matrix to all zeros


# Function to close the application
def closewindow():
    """Closes the application."""
    window.destroy()


# Validation function for input
def validate_input(P):
    """Validates user input to ensure only digits 1-9 or an empty value are allowed."""
    return P == "" or (P.isdigit() and len(P) == 1)


# Create the Sudoku grid using Entry widgets
valid_input = (window.register(validate_input), '%P')  # Validation command
for row in range(9):
    for col in range(9):
        entry = tk.Entry(
            window,
            width=2,
            font=('Helvetica', 14),
            justify='center',
            validate='key',
            validatecommand=valid_input,
        )
        entry.grid(row=row, column=col, padx=5, pady=5)  # Place the Entry widget on the grid
        entry_widgets[row][col] = entry  # Store the Entry widget reference


# Create buttons for "Solve", "Reset", and "Close"
button_solve = tk.Button(
    window,
    text="Solve",
    command=solvesudoku,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=10,
)
button_solve.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

button_reset = tk.Button(
    window,
    text="Reset",
    command=reset_window,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=10,
)
button_reset.grid(row=10, column=3, columnspan=3, padx=10, pady=10)

button_close = tk.Button(
    window,
    text="Close",
    command=closewindow,
    bg="#B3DAF1",
    fg="#1F3A93",
    activebackground="#0F3057",
    font=("Helvetica", 14),
    width=10,
)
button_close.grid(row=10, column=6, columnspan=3, padx=10, pady=10)


# Run the Tkinter application
if __name__ == "__main__":
    window.mainloop()
