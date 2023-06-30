# Simple 2048
# Marcus Secu
# 2023-1-31

"""A simple version of 2048, made with the 'tkinter' window manager in Python."""

import tkinter, random

# Initialize window
root = tkinter.Tk()
root['bg'] = "#101010"
root.title("2048")
root.geometry("420x500")

# Set up logic board
board = [[0]*4 for y in range(0, 4)]
board[random.randrange(0, 4)][random.randrange(0, 4)] = random.randrange(2, 5, 2)

# Colors for tiles
colors = {
    2: '#ffebeb',
    4: '#ffe1e1',
    8: '#ffc3c3',
    16: '#ff9b9b',
    32: '#ff8787',
    64: '#ff7373',
    128: '#ff5f5f',
    256: '#ff4b4b',
    512: '#ff3737',
    1024: '#ff2323',
    2048: '#ff0f0f',
}

# Game-keeping variables
score = 0
game_state = 'run'

def update_game(event):
    """Update board, change score, and check if game is over given user input."""
    global board, game_state
    
    # Quit game if 'q' key is pressed
    if event.keysym == 'q':

        root.quit()
        return

    # Game over display
    if game_state != "run":
        reset_button.pack(side="bottom")
        score_display['font'] = ("Arial", 20)
        if game_state == 'win':
            score_display['text'] = F"YOU WIN! :)\nFINAL SCORE: {score}"
        elif game_state == 'lose':
            score_display['text'] = F"GAME OVER!\nFINAL SCORE: {score}"
        return

    new_board = []

    # compress board and update score in direction indicated by user
    match event.keysym:
        case "d":
            new_board = compress_board_right(board)
        case "a":
            new_board = compress_board_left(board)
        case "w":
            new_board = compress_board_up(board)
        case "s":
            new_board = compress_board_down(board)

    # If there are any empty spots in board, randomly populate one,
    # else declare the game to be over.
    empty_spots = []
    for row in enumerate(new_board):
        for col in enumerate(row[1]):
            if col[1] == 0:
                empty_spots.append([row[0], col[0]])

    
    for row in new_board:
        if game_state == 'win':
            break
        for col in row:
            if col == 2048:
                reset_button.pack(side='bottom')
                game_state = "win"
                score_display['font'] = ("Arial", 20)
                score_display['text'] = F"YOU WIN! :)\nFINAL SCORE: {score}"
                if len(empty_spots):
                    random_spot = empty_spots[random.randrange(0, len(empty_spots))]
                    new_board[random_spot[0]][random_spot[1]] = random.randrange(2, 5, 2)
                board = new_board

                for row in enumerate(board):
                    for col in enumerate(row[1]):
                        if col[1] != 0:
                            board_spots[row[0]][col[0]][1]['text'] = col[1]
                            board_spots[row[0]][col[0]][1]['bg'] = colors[col[1]]
                        else:
                            board_spots[row[0]][col[0]][1]['text'] = ''
                            board_spots[row[0]][col[0]][1]['bg'] = '#fff5f5'
                return

    if len(empty_spots):
        random_spot = empty_spots[random.randrange(0, len(empty_spots))]
        new_board[random_spot[0]][random_spot[1]] = random.randrange(2, 5, 2)
    else:
        game_state = 'lose' if game_state != 'win' else game_state
    
    # Update real board and score text
    board = new_board
    score_display['text'] = F"SCORE: {score}"
    
    for row in enumerate(board):
        for col in enumerate(row[1]):
            if col[1] != 0:
                board_spots[row[0]][col[0]][1]['text'] = col[1]
                board_spots[row[0]][col[0]][1]['bg'] = colors[col[1]]
            else:
                board_spots[row[0]][col[0]][1]['text'] = ''
                board_spots[row[0]][col[0]][1]['bg'] = '#fff5f5'

def compress_board_left(board):
    """Move all board numbers to the left and compress like numbers."""
    global score
    new_board = [[0]*4 for y in range(4)]

    # Iterate through board from left to right
    for y in range(4):
        last_pos = 0
        for x in range(4):
 
            if board[y][x] != 0:

                # If current number is equal to the one on its left, combine and double them.
                # Else, just move it all the way to the left.
                if last_pos > 0 and new_board[y][last_pos-1] == board[y][x]:
                    new_board[y][last_pos-1] *= 2
                    score += new_board[y][last_pos-1]
                    continue

                new_board[y][last_pos] = board[y][x]

                last_pos += 1

    return new_board

def compress_board_right(board):
    """Move all board numbers to the right and compress like numbers."""
    global score
    new_board = [[0]*4 for y in range(4)]

    # Iterate through board from right to left
    for y in range(3, -1, -1):
        last_pos = 3
        
        for x in range(3, -1, -1):

            if board[y][x] != 0:

                # If current number is equal to the one on its right, combine and double them.
                # Else, just move it all the way to the right.
                if last_pos < 3 and new_board[y][last_pos+1] == board[y][x]:
                    new_board[y][last_pos+1] *= 2
                    score += new_board[y][last_pos+1]
                    continue

                new_board[y][last_pos] = board[y][x]

                last_pos -= 1

    return new_board

def compress_board_up(board):
    """Move all board numbers to the top and compress like numbers."""
    global score
    new_board = [[0]*4 for y in range(4)]

    # Iterate through board from top to bottom
    for x in range(4):

        last_pos = 0
        for y in range(4):

            if board[y][x] != 0:

                # If current number is equal to the one above it, combine and double them.
                # Else, just move it all the way up.
                if last_pos > 0 and new_board[last_pos-1][x] == board[y][x]:
                    new_board[last_pos-1][x] *= 2
                    score += new_board[last_pos-1][x]
                    continue

                new_board[last_pos][x] = board[y][x]
                last_pos += 1
                
    return new_board

def compress_board_down(board):
    """Move all board numbers to the bottom and compress like numbers."""
    global score
    new_board = [[0]*4 for y in range(4)]

    # Iterate through board from bottom to top
    for x in range(3, -1, -1):

        last_pos = 3
        for y in range(3, -1, -1):

            if board[y][x] != 0:

                # If current number is equal to the one below it, combine and double them.
                # Else, just move it all the way down.
                if last_pos < 3 and new_board[last_pos+1][x] == board[y][x]:
                    new_board[last_pos+1][x] *= 2
                    score += new_board[last_pos+1][x]
                    continue

                new_board[last_pos][x] = board[y][x]
                last_pos -= 1
                
    return new_board

def reset_game():
    """Reset all game values to original."""
    global board, score, board, game_state
    reset_button.pack_forget()
    score = 0
    board = [[0]*4 for y in range(0, 4)]
    board[random.randrange(0, 4)][random.randrange(0, 4)] = random.randrange(2, 5, 2)
    for row in enumerate(board):
        for col in enumerate(row[1]):
            if col[1] != 0:
                board_spots[row[0]][col[0]][1]['text'] = col[1]
                board_spots[row[0]][col[0]][1]['bg'] = colors[col[1]]
            else:
                board_spots[row[0]][col[0]][1]['text'] = ''
                board_spots[row[0]][col[0]][1]['bg'] = '#fff5f5'

    game_state = 'run'
    score_display['font'] = ("Arial", 14)
    score_display['text'] = F"SCORE: {score}"

# Set up main display
main_display = tkinter.Frame(root)

# Set up info display
score_display = tkinter.Label(main_display, font=("Arial", 14), text="SCORE: 0")
score_display.pack(side='top')

# Reset button
reset_button = tkinter.Button(main_display, text="RESTART", command=reset_game)

# Set up board display
board_display = tkinter.Frame(main_display, padx=3, pady=3) 
board_display['bg'] = "#505050"
board_spots = []

for row in range(4):
    board_spots.append([])

    for col in range(4):

        board_spots[row].append([tkinter.Frame(board_display)])
        board_spots[row][col].append(tkinter.Label(board_spots[row][col][0], text='', font=("Arial", 25), width=4, height=2))
        if board[row][col]:

            board_spots[row][col][1]['text'] = board[row][col]
        
        board_spots[row][col][1].pack()
        board_spots[row][col][1]['bg'] = '#fff5f5'
        board_spots[row][col][0].grid(column=col, row=row, padx=6, pady=6)

board_display.pack(side='top')

# Set up info display
info_display = tkinter.Label(main_display, font=("Arial", 10), text="WASD to move board, get to 2048 to win. Good luck!")
info_display.pack(side="bottom")

main_display.pack(pady=5)

root.bind("<Key>", update_game)
root.mainloop()