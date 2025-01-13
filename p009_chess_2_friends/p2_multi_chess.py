# bugs:
#     1. game ends with king killed (No Checkmates, stalemates and Draws)
#     2. Can not make pins or discovery

import pygame

pygame.init()

width = 1080
height = 780
square_number = 8
square_size = height*0.85/square_number
piece_size = square_size*0.85
light_color = "#eeeed2"
dark_color = "#769656"
bg_color = "#d6d6b8"
boder_color = "#4e5c39"
x_offset = ((width-(square_size*8))/2)-20
y_offset = ((height-(square_size*8))/2)


screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Solitaire Chess')
font = pygame.font.Font('freesansbold.ttf',20)
title_font = pygame.font.Font('freesansbold.ttf',30)
big_font = pygame.font.Font('freesansbold.ttf',50)

timer = pygame.time.Clock()
fps = 60

# game variable and images
white_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
white_location = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                  (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),]

black_pieces = ['rook','knight','bishop','queen','king','bishop','knight','rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
black_location = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                  (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),]

captured_pieces_white = []
captured_pieces_black = []

# 0 is white; 1 is black
turn_step = 0
selection = 100
valid_moves = []

# load images
black_queen = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-queen.png'), (piece_size, piece_size))
black_queen_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-queen.png'), (piece_size/2, piece_size/2))
white_queen = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-queen.png'), (piece_size, piece_size))
white_queen_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-queen.png'), (piece_size/2, piece_size/2))

black_king = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-king.png'), (piece_size, piece_size))
black_king_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-king.png'), (piece_size/2, piece_size/2))
white_king = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-king.png'), (piece_size, piece_size))
white_king_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-king.png'), (piece_size/2, piece_size/2))

black_rook = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-rook.png'), (piece_size, piece_size))
black_rook_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-rook.png'), (piece_size/2, piece_size/2))
white_rook = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-rook.png'), (piece_size, piece_size))
white_rook_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-rook.png'), (piece_size/2, piece_size/2))

black_knight = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-knight.png'), (piece_size, piece_size))
black_knight_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-knight.png'), (piece_size/2, piece_size/2))
white_knight = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-knight.png'), (piece_size, piece_size))
white_knight_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-knight.png'), (piece_size/2, piece_size/2))

black_bishop = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-bishop.png'), (piece_size, piece_size))
black_bishop_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-bishop.png'), (piece_size/2, piece_size/2))
white_bishop = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-bishop.png'), (piece_size, piece_size))
white_bishop_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-bishop.png'), (piece_size/2, piece_size/2))

black_pawn = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-pawn.png'), (piece_size, piece_size))
black_pawn_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/black-pawn.png'), (piece_size/2, piece_size/2))
white_pawn = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-pawn.png'), (piece_size, piece_size))
white_pawn_small = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/white-pawn.png'), (piece_size/2, square_size/2))

player_white = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/engine_black.png'), (piece_size*0.80, piece_size*0.80))
player_black = pygame.transform.scale(pygame.image.load('a9 Chess easy/images/engine_white.png'), (piece_size*0.80, piece_size*0.80))

white_images = [white_king, white_queen, white_rook, white_knight, white_bishop, white_pawn]
black_images = [black_king, black_queen, black_rook, black_knight, black_bishop, black_pawn]

small_white_images = [white_king_small, white_queen_small, white_rook_small, white_knight_small, white_bishop_small, white_pawn_small]
small_black_images   = [black_king_small, black_queen_small, black_rook_small, black_knight_small, black_bishop_small, black_pawn_small]

piece_list = ['king', 'queen', 'rook', 'knight', 'bishop', 'pawn']

# check variable/ flashing counter
counter = 0

#----------------------------------------------------------------------------------------------------------------------------------#
# drawing main game board
def draw_board():
    screen.blit(player_white, ( x_offset + 10, 2.5))
    screen.blit(title_font.render("Rakash Raj", True, boder_color), (x_offset+square_size-10, 17.5))

    screen.blit(player_black, (x_offset + 10 , y_offset+(square_size*8)+2.5))
    screen.blit(title_font.render("Indra Raj", True, boder_color), (x_offset+square_size-10, y_offset+(square_size*8)+17.5))

    for row in range(square_number):
        for col in range(square_number):
            color = light_color if (row + col) % 2 == 0 else dark_color
            pygame.draw.rect(screen, color, ((col * square_size) + x_offset, (row * square_size) + y_offset, square_size, square_size))


    status_text = ["White : Select Piece", "White : destination?", "Black : Select Piece", "Black : destination?"]
    
    if "White" in status_text[turn_step]:
        screen.blit(font.render(status_text[turn_step], True, dark_color), ((square_size*8)+x_offset+25, (square_size*8)+y_offset+20))
    else:
        screen.blit(font.render(status_text[turn_step], True, dark_color), ((square_size*8)+x_offset+25, 20))

# put pieces on the board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_location[i][0]*square_size +(piece_size/10) + x_offset, white_location[i][1]*square_size + (piece_size/10) + y_offset))
        # Will show selection
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, boder_color, [(white_location[i][0] * square_size)+x_offset,  (white_location[i][1] * square_size)+y_offset, square_size, square_size],2)


    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_location[i][0]*square_size +(piece_size/10) + x_offset, black_location[i][1]*square_size +(piece_size/10) + y_offset))

         # Will show selection
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, boder_color, [(black_location[i][0]*square_size)+x_offset, (black_location[i][1]*square_size) + y_offset, square_size, square_size],2)

# drawing possible moves on screen
def draw_valid(moves):
    circle_color = (82, 98, 66, 0)

    for i in range(len(moves)):
        pygame.draw.circle(screen, circle_color, ((moves[i][0]*square_size+(square_size/2))+x_offset, (moves[i][1]*square_size+(square_size/2))+y_offset), 10)

# drawing captured pieces
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], ((square_size*8)+ x_offset + 25, (5+50*i)+50))

    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (25,5 + (50*i)+50))

# drawing the checks
def draw_check():
    if turn_step < 2:
        king_index = white_pieces.index('king')
        king_location = white_location[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                if counter < 15:
                    pygame.draw.rect(screen, 'dark red', [white_location[king_index][0] * square_size +x_offset, white_location[king_index][1] * square_size +y_offset, square_size, square_size], 5)

    else:
        king_index = black_pieces.index('king')
        king_location = black_location[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                if counter < 15:
                    pygame.draw.rect(screen, 'dark blue', [black_location[king_index][0] * square_size + x_offset, black_location[king_index][1] * square_size + y_offset, square_size, square_size], 5)


#----------------------------------------------------------------------------------------------------------------------------------#





#----------------------------------------------------------------------------------------------------------------------------------#
# check valid pawn moves
def check_pawn(position, color):

    moves_list = []
    if color == 'white':
        if ((position[0], position[1] - 1) not in white_location) and ((position[0], position[1] - 1) not in black_location) and (position[1] > 0):
            moves_list.append((position[0], position[1] - 1))

        if ((position[0], position[1] - 2) not in white_location) and ((position[0], position[1] - 2) not in black_location) and ((position[0], position[1] - 1) not in white_location) and ((position[0], position[1] - 1) not in black_location) and (position[1] == 6):
            moves_list.append((position[0], position[1] - 2))

        if (position[0] + 1, position[1] - 1) in black_location:
            moves_list.append((position[0] + 1, position[1] - 1))

        if (position[0] - 1, position[1] - 1) in black_location:
            moves_list.append((position[0] - 1, position[1] - 1))


    else:
        if ((position[0], position[1] + 1) not in white_location) and ((position[0], position[1] + 1) not in black_location) and (position[1] < 7):
            moves_list.append((position[0], position[1] + 1))

        if ((position[0], position[1] + 2) not in white_location) and ((position[0], position[1] + 2) not in black_location) and ((position[0], position[1] + 1) not in white_location) and ((position[0], position[1] + 1) not in black_location) and (position[1] == 1):
            moves_list.append((position[0], position[1] + 2))

        if (position[0] + 1, position[1] + 1) in white_location:
            moves_list.append((position[0] + 1, position[1] + 1))

        if (position[0] - 1, position[1] + 1) in white_location:
            moves_list.append((position[0] - 1, position[1] + 1))

    return moves_list

# check valid rook moves
def check_rook(position,color): 
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location
    for i in range(4): # left right up down
        path = True
        chain = 1

        if i == 0:
            x = 0
            y = 1

        elif i == 1:
            x = 0
            y = -1
        
        elif i == 2:
            x = 1
            y = 0
        
        else:
            x = -1
            y = 0
        
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and 0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain * y) <=7:
                moves_list.append((position[0] + (chain*x), position[1]+(chain*y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1    

            else:
                path = False    

    return moves_list

# check valid knight moves
def check_knight(position,color):
    moves_list = []

    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location

    # 8 sqaures to check for kinght, 
    targets = [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]

    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0<= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list

# check valid bishop moves
def check_bishop(position,color):
    moves_list = []

    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location
    
    for i in range(4): # up_right, up_left, down right, down left
        path = True
        chain = 1

        if i == 0:  # right up
            x = 1
            y = -1

        elif i == 1: # left up
            x = -1
            y = -1
        
        elif i == 2: # right down
            x = 1
            y = 1
        
        else:
            x = -1 # left down
            y = 1

        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and 0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain * y) <=7:
                moves_list.append((position[0] + (chain*x), position[1]+(chain*y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1    

            else:
                path = False

    return moves_list

# check valid queen moves
def check_queen(position,color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position,color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])

    return moves_list

# check valid king moves
def check_king(position,color):
    moves_list = []

    if color == 'white':
        enemies_list = black_location
        friends_list = white_location
    else:
        friends_list = black_location
        enemies_list = white_location

    targets = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0<= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target) 

    return moves_list

#----------------------------------------------------------------------------------------------------------------------------------#





#----------------------------------------------------------------------------------------------------------------------------------#
# check all the valid option on the board
def check_options(pieces, locations, turn):
    move_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            move_list = check_pawn(location, turn)
        
        elif piece == 'rook':
            move_list = check_rook(location, turn)

        elif piece == 'knight':
            move_list = check_knight(location, turn)

        elif piece == 'bishop':
            move_list = check_bishop(location, turn)
            
        elif piece == 'queen':
            move_list = check_queen(location, turn)
        
        elif piece == 'king':
            move_list = check_king(location, turn)

        all_moves_list.append(move_list)
    return all_moves_list

# check for valid moves for just selected pieces
def check_valid_moves():
    if turn_step < 2:
        option_list = white_options

    else:
        option_list = black_options

    valid_options = option_list[selection]
    return valid_options

#----------------------------------------------------------------------------------------------------------------------------------#





#----------------------------------------------------------------------------------------------------------------------------------#

black_options = check_options(black_pieces, black_location, 'balck')
white_options = check_options(white_pieces, white_location, 'white')

# Main Loop
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0

    screen.fill(bg_color)
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # on a left mouse click
            x_coord = (event.pos[0] - x_offset) // square_size
            y_coord = (event.pos[1] - y_offset) // square_size
            click_coord = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coord in white_location :
                    selection = white_location.index(click_coord)
                    if turn_step == 0:
                        turn_step = 1
                if click_coord in valid_moves and selection != 100:
                    white_location[selection] = click_coord
                    if click_coord in black_location:
                        black_piece = black_location.index(click_coord)
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_location.pop(black_piece)
                    black_options = check_options(black_pieces, black_location, 'balck')
                    white_options = check_options(white_pieces, white_location, 'white')

                    turn_step = 2
                    selection = 100
                    valid_moves = []

            if turn_step > 1:
                if click_coord in black_location :
                    selection = black_location.index(click_coord)
                    if turn_step == 2:
                        turn_step = 3
                if click_coord in valid_moves and selection != 100:
                    black_location[selection] = click_coord
                    if click_coord in white_location:
                        white_piece = white_location.index(click_coord)
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_location.pop(white_piece)
                    black_options = check_options(black_pieces, black_location, 'balck')
                    white_options = check_options(white_pieces, white_location, 'white')

                    turn_step = 0
                    selection = 100
                    valid_moves = []


    # Update the display
    pygame.display.flip()

pygame.quit()


