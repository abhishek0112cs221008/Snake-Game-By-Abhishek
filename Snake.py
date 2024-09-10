import pygame
import random
import os

pygame.mixer.init()

pygame.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
lightYellow = (255, 254, 219)
green = (76, 176, 70)
pink = (255, 219, 238)
yellow = (255, 255, 0)

#creating windows
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("images/bg.jpg")
bgimg2 = pygame.image.load("images/bg2.jpg")
bgimgStart = pygame.image.load("images/startGame.jpg")
bgimgOver = pygame.image.load("images/game_over.jpg")
snakeImg = pygame.image.load("images/snake.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
bgimgStart = pygame.transform.scale(bgimgStart, (screen_width, screen_height)).convert_alpha()
bgimgOver = pygame.transform.scale(bgimgOver, (screen_width, screen_height)).convert_alpha()
snakeImg = pygame.transform.smoothscale(snakeImg, (100, 90)).convert_alpha()
bgimg2 = pygame.transform.smoothscale(bgimg2, (200, 190)).convert_alpha()


# Game Title
pygame.display.set_caption("Snakes Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# button
def button(button_color, button_text, button_rect):
    font = pygame.font.SysFont(None, 36)
    # Draw button
    pygame.draw.rect(gameWindow, button_color, button_rect)
    text_surface = font.render(button_text, True, (255, 255, 255))
    gameWindow.blit(text_surface, (button_rect.x + 50, button_rect.y + 15))
    pygame.display.update()

# front page
def welcome():
    exit_game = False
    while not exit_game:
        # gameWindow.fill((233,210,229))
        # gameWindow.fill(white)
        gameWindow.blit(bgimgStart, (0, 0))
        gameWindow.blit(snakeImg, (100, 240))
        text_screen("Welcome to Snakes", pink, 225, 250)
        text_screen("Press Space Bar To Play", red, 200, 290)

        # gameWindow.blit(bgimg2, (10, 10))
        # text_screen("PLAY & FUN", red, 10, 10)

        # Define button properties
        button_rect = pygame.Rect(100, 100, 200, 50)
        button_color = (255, 0, 0)
        button(button_color,"Play Game",button_rect)

        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                exit_game = True             
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Button clicked, start the game
                    # print("Game started!")
                    pygame.mixer.music.load('audio/bg_music_1.mp3')
                    pygame.mixer.music.play()
                    gameloop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('audio/bg_music_1.mp3')
                    pygame.mixer.music.play()
                    gameloop()

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width)
    food_y = random.randint(20, screen_height)
    score = 0
    init_velocity = 5
    snake_size = 30
    snake_sizeF = 28
    fps = 60

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimgOver, (0, 0))
            
            text_screen("Score: " + str(score) + "    Hiscore: "+str(hiscore), green,190, 450)
            text_screen("Press Enter To Continue!", red, 190, 500)
            button_rect = pygame.Rect(100, 100, 200, 50)
            button(green, "Play Again", button_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        welcome()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # if event.key == pygame.K_q:
                    #     score +=10                   #cheating

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<15 and abs(snake_y - food_y)<15:
                score +=10
                food_x = random.randint(20, screen_width)
                food_y = random.randint(20, screen_height)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_sizeF, snake_sizeF])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('audio/gameover.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('audio/gameover.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, yellow, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()