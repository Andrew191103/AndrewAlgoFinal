import pygame
import random
from pygame import mixer
import button
#pygame: A library for making games and other multimedia applications with Python.
#random: A library that generates pseudo-random numbers.
#mixer: A library from Pygame that is used for loading and playing sounds.
#button: A library that you created to handle button functionality, it is not part of the python standard library.

pygame.init()

#create display window
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Andrews 2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
#This code creates a window with the specified width and height using the Pygame library.
#The window is titled "Andrews 2048" and the font for the text in the window is set to "freesansbold.ttf" with a size of 24.
#The "timer" variable is used to control the frame rate of the window, which is set to 60 frames per second.


# 2048 game color library
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (187, 173, 160)
}
#Each key in the dictionary corresponds to a tile value (e.g. 2, 4, 8, etc.)
#and the value for that key is a tuple of 3 integers representing the red, green, and blue values of the color.
#The dictionary also includes colors for the text, other elements, and background of the game.
#These colors will be used to display the different number tiles and other elements in the game.
# main game loop

# Load button images
start_img = pygame.image.load('start.png').convert_alpha()
exit_img = pygame.image.load('exit.png').convert_alpha()

# Create button instances
start_button = button.Button(85, 150, start_img, 0.4)
exit_button = button.Button(85, 300, exit_img, 0.4)

gamerun = False
run = True

while run:
    screen.fill((202, 228, 241))

    if start_button.draw(screen):
        gamerun = True
        run = False
    if exit_button.draw(screen):
        pygame.quit()
    # This code runs the main loop of the game, which will continue to execute as long as the variable "run" is set to True.
    # If the start button is clicked, the text "START" will be printed to the console,
    # and if the exit button is clicked, the text "EXIT" will be printed to the console.

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
#Background sound
mixer.music.load('Background.wav')
mixer.music.play(-1)
#This code uses the Pygame library's "mixer" module to play background music for the game.
#The music file, "Background.wav", is loaded using the "load" function
# and the "play" function is called with the argument "-1" which causes the music to loop indefinitely.

#Load button images
start_img = pygame.image.load('start.png').convert_alpha()
exit_img = pygame.image.load('exit.png').convert_alpha()
#This code loads button images "start.png" and "exit.png" using the Pygame library's "image" module.
#These images will be used for the start and exit buttons for the game.

#create button instances
start_button = button.Button(85,150, start_img, 0.4)
exit_button = button.Button(85, 300, exit_img, 0.4)
#This code creates instances of the class "Button" from the "button" module.
#these instances of the class will be used to create the start and exit buttons that will be displayed on the screen.


# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
#This code initializes several variables for the game.
#The board_values variable is a 4x4 2D list filled with 0s, representing the initial state of the game board.
#The game_over variable is set to False, indicating that the game is not over.
#The spawn_new variable is set to True, indicating that a new tile needs to be spawned on the board.
#The init_count variable is set to 0, it's purpose is not clear.
#The direction variable is set to an empty string, indicating that no direction has been chosen yet.
# which is the high score obtained from the file.


# draw game over and restart text
def draw_over():
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    text_rect1 = game_over_text1.get_rect(center=(200, 70))
    text_rect2 = game_over_text2.get_rect(center=(200, 120))
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0)
    screen.blit(game_over_text1, text_rect1)
    screen.blit(game_over_text2, text_rect2)
#This code defines a function draw_over() that is used to display "Game Over!"
#and "Press Enter to Restart" text when the game is over.
#Inside the function, it uses the font.render() method to create a surface with the text "Game Over!"
#and "Press Enter to Restart" rendered on it, with the color white.
#The get_rect() method is used to get the rectangle containing the text, which is then centered at (200, 70)
#and (200, 120) for the first and second text respectively.
#The text is then drawn on the screen using the screen.blit() method, passing the text surface and the rectangle as arguments.


# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board
#This code defines a function take_turn() which takes in the direction of the turn and the current state of the board as arguments.
#The function updates the board based on the direction of the turn and returns the updated board.
#The function starts by initializing a 2D list merged filled with False values.
#This list will be used to keep track of which tiles have been merged in the current turn.
#The function then checks the direction of the turn and uses nested loops to iterate through the board.
#The function also makes use of the global variable score to update the score of the player.
#It's important to note that the function modifies the board passed as an argument
#and doesn't create a copy of it, so the original board will be modified.





# spawn in new pieces randomly when turns start
def new_pieces(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty_cells:
        return board, True
    cell = random.choice(empty_cells)
    board[cell[0]][cell[1]] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
    return board, False
#This code defines a function new_pieces() which takes in the current state of the board as an argument
#and spawns new pieces randomly on the board.
#The function starts by creating a list of tuples called empty_cells containing
#the coordinates of all the empty cells on the board (cells with value 0).
#If there are empty cells, the function chooses a random empty cell using the random.choice() function
#and assigns a random value of 2 or 4 to it using random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4]).
#Finally, the function returns the updated board and a boolean value of False,
#which would indicate that the board is not full.

# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    score_rect = score_text.get_rect(topleft=(10, 410))
    high_score_rect = high_score_text.get_rect(topleft=(10, 450))
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, high_score_rect)
#This code defines a function draw_board() which is used to draw the background for the game board.
#The function starts by using the pygame.draw.rect() function to draw a rectangle on
#the screen with the top left corner at (0, 0), width 400 and height 400
#Finally, the text is drawn on the screen using the screen.blit() method,
#passing the text surface and the rectangle as arguments.


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0)
            if value > 0:
                value_len = len(str(value))
                font_size = 48 - (5 * value_len)
                font = pygame.font.Font('freesansbold.ttf', font_size)
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2)
#This code defines a function draw_pieces() which takes in the current state of the board as
#an argument and draws the tiles for the game.
#It then checks if the cell value is greater than 0, if so it will render the value of the cell in the center of the rectangle using the font.render() method,
#with the color of the text determined by whether the value is less than or equal to 8.
#Then it will adjust the font size of the text according to the length of the value of the cell.
#It's important to note that the function draws the rectangles and text directly on the screen variable, so it needs to be called after the background is drawn.
#Finally, it uses the pygame.draw.rect() function to draw a rectangle on the screen with the top left corner at width 75 and height 75, and filled with the color black, which will be the outline of each tile.


while gamerun:
    # This code handles the events that occur during the execution of the game.
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()
