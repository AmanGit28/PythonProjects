

#  ----------------------------------------- Still work in progress ----------------------------------------- #



import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600  # Size of the window
BOARD_SIZE = 8  # 8x8 chessboard
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE  # Size of each square
LIGHT_COLOR = (240, 217, 181)  # Light square color (beige)
DARK_COLOR = (181, 136, 99)  # Dark square color (brown)
# Handle player actions
selected_piece = None
selected_pos = None
player_turn = "white"

king_positions = {
    "white_king": (4, 7),  # Initial position of the white king
    "black_king": (4, 0)   # Initial position of the black king
}


# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chessboard with Pieces")

# Load and scale piece images
piece_images = {
    "white_pawn": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/white-pawn.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "black_pawn": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/black-pawn.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "white_rook": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/white-rook.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "black_rook": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/black-rook.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "white_knight": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/white-knight.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "black_knight": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/black-knight.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "white_bishop": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/white-bishop.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "black_bishop": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/black-bishop.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "white_queen": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/white-queen.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "black_queen": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/black-queen.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "white_king": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/white-king.png"), (SQUARE_SIZE, SQUARE_SIZE)),
    "black_king": pygame.transform.scale(pygame.image.load("a9 Chess easy/images/black-king.png"), (SQUARE_SIZE, SQUARE_SIZE)),
}

# Define initial positions for all pieces
initial_positions = {
    "white_pawn": [(x, 6) for x in range(8)],
    "black_pawn": [(x, 1) for x in range(8)],
    "white_rook": [(0, 7), (7, 7)],
    "black_rook": [(0, 0), (7, 0)],
    "white_knight": [(1, 7), (6, 7)],
    "black_knight": [(1, 0), (6, 0)],
    "white_bishop": [(2, 7), (5, 7)],
    "black_bishop": [(2, 0), (5, 0)],
    "white_queen": [(3, 7)],
    "black_queen": [(3, 0)],
    "white_king": [(4, 7)],
    "black_king": [(4, 0)],
}

# Track whether the kings and rooks have moved
castling_flags = {
    "white_king": False,
    "black_king": False,
    "white_rook_king_side": False,
    "white_rook_queen_side": False,
    "black_rook_king_side": False,
    "black_rook_queen_side": False,
}

# Track pawn movement state
pawn_moved = {
    pos: False for pos in initial_positions["white_pawn"] + initial_positions["black_pawn"]
    }

# -------------------------- Set up the board -------------------------- #
# Function to draw the chessboard
def draw_chessboard():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw pieces on the board
def draw_pieces():
    for piece, positions in initial_positions.items():
        for (col, row) in positions:
            screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def positions_of_pieces():
    positions = []
    for p, pos_list in initial_positions.items():
        positions.extend(pos_list)
    return positions

# Function to get all positions occupied by pieces
def positions_of_pieces():
    positions = []
    for piece, positions_list in initial_positions.items():
        positions.extend(positions_list)
    return positions


# -------------------------- Checking the condition -------------------------- #
# Function to check if the path is clear (used for two-square pawn moves)
def is_path_clear(start_pos, end_pos):
    start_col, start_row = start_pos
    end_col, end_row = end_pos
    
    if start_col == end_col:  # Vertical castling (queen-side or king-side)
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if (start_col, row) in positions_of_pieces():
                return False
    elif start_row == end_row:  # Horizontal castling
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if (col, start_row) in positions_of_pieces():
                return False
    return True

# Function to check if the path is clear for rook or queen (horizontal or vertical)
def is_path_clear_for_rook_or_queen(old_pos, new_pos):
    old_col, old_row = old_pos
    new_col, new_row = new_pos
    
    if old_col == new_col:  # Vertical move
        step = 1 if new_row > old_row else -1
        for row in range(old_row + step, new_row, step):
            if (old_col, row) in positions_of_pieces():
                return False  # Blocked by another piece
    elif old_row == new_row:  # Horizontal move
        step = 1 if new_col > old_col else -1
        for col in range(old_col + step, new_col, step):
            if (col, old_row) in positions_of_pieces():
                return False  # Blocked by another piece
    return True

# Function to check if the path is clear for diagonal moves (bishop and queen)
def is_path_clear_for_diagonal(old_pos, new_pos):
    old_col, old_row = old_pos
    new_col, new_row = new_pos

    direction_col = 1 if new_col > old_col else -1
    direction_row = 1 if new_row > old_row else -1

    col, row = old_col + direction_col, old_row + direction_row
    while (col != new_col) and (row != new_row):
        if (col, row) in positions_of_pieces():
            return False  # Blocked by another piece
        col += direction_col
        row += direction_row
    return True

# Function to check if sqaure is under attack or not
def is_square_under_attack(square, opponent_color):
    # Loop through all the opponent's pieces to check if any can attack the square
    for p, positions in initial_positions.items():
        if p.startswith(opponent_color):  # Only check pieces of the opponent
            for pos in positions:
                if is_valid_move(pos, square, p):  # Check if this piece can attack the square
                    return True
    return False

def is_king_in_check(player_color):
    king_pos = None
    # Find the king's position
    for piece, positions in initial_positions.items():
        if piece == f"{player_color}_king":
            king_pos = positions[0]  # Kings have a single position
            break

    if not king_pos:
        return False  # If no king is found (shouldn't happen)

    # Check if any opposing piece can attack the king's position
    opponent_color = "black" if player_color == "white" else "white"
    for piece, positions in initial_positions.items():
        if piece.startswith(opponent_color):
            for pos in positions:
                if is_valid_move(piece, pos, king_pos):
                    return True  # King is in check
    return False


# -------------------------- Validates the move -------------------------- #
def is_valid_move(piece, old_pos, new_pos):
    old_col, old_row = old_pos
    new_col, new_row = new_pos

    # Check if the target square is occupied by a piece of the same color
    for p, positions in initial_positions.items():
        if (new_col, new_row) in positions:
            if p.startswith(piece.split('_')[0]):  # Same color, invalid move
                return False

    # Pawn movement rules
    if piece == "white_pawn":
        # Forward move
        if new_row == old_row - 1 and new_col == old_col:  # Move one step forward
            if (new_col, new_row) not in positions_of_pieces():
                return True
        if new_row == old_row - 2 and new_col == old_col and not pawn_moved[old_pos]:  # First move, two squares forward
            if is_path_clear(old_pos, (new_col, new_row)) and (new_col, new_row) not in positions_of_pieces():
                return True
    # Diagonal capture
    if new_row == old_row - 1 and abs(new_col - old_col) == 1:  # Diagonal move
        for p, positions in initial_positions.items():
            if (new_col, new_row) in positions and p.startswith("black"):  # Opponent piece
                return True

    elif piece == "black_pawn":
        # Forward move
        if new_row == old_row + 1 and new_col == old_col:  # Move one step forward
            if (new_col, new_row) not in positions_of_pieces():
                return True
        if new_row == old_row + 2 and new_col == old_col and not pawn_moved[old_pos]:  # First move, two squares forward
            if is_path_clear(old_pos, (new_col, new_row)) and (new_col, new_row) not in positions_of_pieces():
                return True
    # Diagonal capture
    if new_row == old_row + 1 and abs(new_col - old_col) == 1:  # Diagonal move
        for p, positions in initial_positions.items():
            if (new_col, new_row) in positions and p.startswith("white"):  # Opponent piece
                return True

    # Bishop movement rules
    elif piece == "white_bishop" or piece == "black_bishop":
        if abs(new_col - old_col) == abs(new_row - old_row):  # Diagonal move
            if is_path_clear_for_diagonal(old_pos, new_pos):
                return True

    # Knight movement rules (L-shape move)
    elif piece == "white_knight" or piece == "black_knight":
        if (abs(new_col - old_col) == 2 and abs(new_row - old_row) == 1) or (abs(new_col - old_col) == 1 and abs(new_row - old_row) == 2):
            return True

    # Rook movement rules
    elif piece == "white_rook" or piece == "black_rook":
        if old_col == new_col or old_row == new_row:  # Horizontal or vertical move
            if is_path_clear_for_rook_or_queen(old_pos, new_pos):
                return True

    # Queen movement rules (combines rook and bishop)
    elif piece == "white_queen" or piece == "black_queen":
        if old_col == new_col or old_row == new_row:  # Horizontal or vertical move
            if is_path_clear_for_rook_or_queen(old_pos, new_pos):
                return True
        elif abs(new_col - old_col) == abs(new_row - old_row):  # Diagonal move
            if is_path_clear_for_diagonal(old_pos, new_pos):
                return True

    # King movement rules (one square in any direction)
    elif piece == "white_king" or piece == "black_king":
        if abs(new_col - old_col) <= 1 and abs(new_row - old_row) <= 1:
            # Check if the king would move into a square under attack
            if is_square_under_attack((new_col, new_row), "black" if piece.startswith("white") else "white"):
                print("Invalid move: The king cannot move into check!")
                return False  # Invalid move, return False
            return True

        # Castling
        if piece == "white_king" and not castling_flags["white_king"] and old_row == 7:
            # King-side castling
            if new_col == 6 and new_row == 7 and not castling_flags["white_rook_king_side"]:
                if is_path_clear((4, 7), (6, 7)) and not is_square_under_attack((5, 7), "black") and not is_square_under_attack((4, 7), "black"):
                    return True
            # Queen-side castling
            if new_col == 2 and new_row == 7 and not castling_flags["white_rook_queen_side"]:
                if is_path_clear((4, 7), (2, 7)) and not is_square_under_attack((3, 7), "black") and not is_square_under_attack((4, 7), "black"):
                    return True

        if piece == "black_king" and not castling_flags["black_king"] and old_row == 0:
            # King-side castling
            if new_col == 6 and new_row == 0 and not castling_flags["black_rook_king_side"]:
                if is_path_clear((4, 0), (6, 0)) and not is_square_under_attack((5, 0), "white") and not is_square_under_attack((4, 0), "white"):
                    return True
            # Queen-side castling
            if new_col == 2 and new_row == 0 and not castling_flags["black_rook_queen_side"]:
                if is_path_clear((4, 0), (2, 0)) and not is_square_under_attack((3, 0), "white") and not is_square_under_attack((4, 0), "white"):
                    return True
    return False



# -------------------------- Movement of piece -------------------------- #
def move_piece(piece, old_pos, new_pos):
    global castling_flags
    old_col, old_row = old_pos
    new_col, new_row = new_pos

    # Check if the target square is occupied by an opponent's piece
    for p, positions in initial_positions.items():
        if (new_col, new_row) in positions:
            if p.startswith(piece.split('_')[0]):  # Same color, invalid move
                return False
            # Remove the captured piece
            initial_positions[p].remove((new_col, new_row))

    # Move the piece
    initial_positions[piece].remove(old_pos)
    initial_positions[piece].append(new_pos)

    # Check if the move puts the player's king in check
    if is_king_in_check(piece.split('_')[0]):
        # Undo the move if it results in check
        initial_positions[piece].remove(new_pos)
        initial_positions[piece].append(old_pos)
        print("Move not allowed: Your king would be in check!")
        return False

    # Update castling flags
    if piece == "white_king":
        castling_flags["white_king"] = True
    elif piece == "black_king":
        castling_flags["black_king"] = True
    elif piece == "white_rook" and old_pos == (0, 7):
        castling_flags["white_rook_queen_side"] = True
    elif piece == "white_rook" and old_pos == (7, 7):
        castling_flags["white_rook_king_side"] = True
    elif piece == "black_rook" and old_pos == (0, 0):
        castling_flags["black_rook_queen_side"] = True
    elif piece == "black_rook" and old_pos == (7, 0):
        castling_flags["black_rook_king_side"] = True

    if piece == "white_king" and abs(new_col - old_col) == 2:  # Castling
        if new_col == 6:  # King-side
            initial_positions["white_rook"].remove((7, 7))
            initial_positions["white_rook"].append((5, 7))
        elif new_col == 2:  # Queen-side
            initial_positions["white_rook"].remove((0, 7))
            initial_positions["white_rook"].append((3, 7))
    elif piece == "black_king" and abs(new_col - old_col) == 2:  # Castling
        if new_col == 6:  # King-side
            initial_positions["black_rook"].remove((7, 0))
            initial_positions["black_rook"].append((5, 0))
        elif new_col == 2:  # Queen-side
            initial_positions["black_rook"].remove((0, 0))
            initial_positions["black_rook"].append((3, 0))

    # Update king position
    if piece == "white_king":
        king_positions["white_king"] = new_pos
    elif piece == "black_king":
        king_positions["black_king"] = new_pos
    
    return True


# -------------------------- Handling of click -------------------------- #
def handle_click(pos):
    global selected_piece, selected_pos, player_turn

    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE

    # If a piece is already selected, handle potential move or re-selection
    if selected_piece:
        # Re-select a different piece
        for piece, positions in initial_positions.items():
            if (col, row) in positions:
                if piece.startswith(player_turn):  # Ensure it's the current player's piece
                    selected_piece = piece
                    selected_pos = (col, row)
                    return

        # Attempt to move the selected piece
        if is_valid_move(selected_piece, selected_pos, (col, row)):
            # Check if this move is valid for the king, especially if it would put the king in check
            if selected_piece.endswith('king'):
                # Before moving the king, check if the target square is under attack
                if is_square_under_attack((col, row), 'black' if player_turn == 'white' else 'white'):
                    print(f"Move invalid! {player_turn}'s king would be under attack!")
                    return  # Don't allow the move if the king would be under attack

            # Now execute the move
            move_piece(selected_piece, selected_pos, (col, row))

            # Check if this move leaves the king in check (post-move check)
            if is_king_in_check(player_turn):
                print(f"Move invalid! {player_turn}'s king is in check.")
                # Undo the move if it results in check
                move_piece(selected_piece, (col, row), selected_pos)
            else:
                # Move is valid, proceed with the turn
                selected_piece = None
                selected_pos = None
                player_turn = "black" if player_turn == "white" else "white"
        else:
            print("Invalid move!")
    else:
        # Select a piece if one exists at the clicked position
        for piece, positions in initial_positions.items():
            if (col, row) in positions:
                if piece.startswith(player_turn):  # Ensure it's the current player's piece
                    selected_piece = piece
                    selected_pos = (col, row)
                else:
                    print(f"It's {player_turn}'s turn!")
                return


def can_escape_check(player_color):
    """ Check if the player's king can escape the check. """
    king_pos = king_positions[f"{player_color}_king"]

    # Try moving the king to all adjacent squares
    for col in range(king_pos[0] - 1, king_pos[0] + 2):
        for row in range(king_pos[1] - 1, king_pos[1] + 2):
            if 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE:
                if is_valid_move(f"{player_color}_king", king_pos, (col, row)):
                    # If the move is valid, check if the king is still in check
                    if not is_square_under_attack((col, row), 'black' if player_color == 'white' else 'white'):
                        return True  # The king can escape by moving to this square

    # Check if any piece can block the check or capture the attacker
    for piece, positions in initial_positions.items():
        if piece.startswith(player_color):  # Only check the player's pieces
            for pos in positions:
                if piece != f"{player_color}_king" and is_valid_move(piece, pos, king_pos):
                    # Check if any piece can capture the attacker
                    if piece.endswith("pawn") or piece.endswith("knight") or piece.endswith("rook") or piece.endswith("queen") or piece.endswith("bishop"):
                        return True

    # If no valid moves to escape check
    return False

def is_checkmate(player_color):
    """ Checks if the current player's king is in checkmate. """
    # Check if the king is in check
    if not is_king_in_check(player_color):
        return False  # The player is not in check, so it cannot be checkmate

    # Check if the player has any legal moves to escape the check
    if can_escape_check(player_color):
        return False  # The king can escape, so it's not checkmate

    return True  # The king is in check and can't escape, so it's checkmate

def display_winner(message):
    font = pygame.font.SysFont('Arial', 40)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing the game





# -------------------------- Main loop ------------------------------- #
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    # Check for checkmate
    if is_checkmate("white"):
        print("Checkmate! Black wins!")
        display_winner("Checkmate! Black wins!")
        running = False
    elif is_checkmate("black"):
        print("Checkmate! White wins!")
        display_winner("Checkmate! White wins!")
        running = False

    # Draw the chessboard and pieces
    draw_chessboard()
    if selected_pos:
        pygame.draw.rect(screen, (0, 255, 0), (selected_pos[0] * SQUARE_SIZE, selected_pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
    draw_pieces()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
