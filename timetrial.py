import time, random
import pygame
import pickle
import tkinter 
import tkinter.messagebox
# DEFAULT VALUES
BLOCK_SIZE = 20
FPS = 15
DIFF = "easy"
# COLOURS
BACKGROUND = (255, 255, 255)
BLACK = (0, 0, 0)
APPLE = (255, 0, 0)
SNAKE1 = (0, 155, 0)

# CLOCK
clock = pygame.time.Clock()

# DISPLAY DIMENSIONS
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600


def singleplayer(difficulty: str, alloted_time: int):
    """
    Initializes the gameLoop with the necessary parameters as well as sets the
    difficulty
    :param difficulty:
    :return:
    """
    global FPS
    global DIFF
    DIFF = difficulty
    if difficulty is "easy":
        FPS = 15
    elif difficulty is "medium":
        FPS = 25
    elif difficulty is "hard":
        FPS = 40
    else:  # difficulty is nightmare
        FPS = 60

    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Slither")
    score = gameLoop(False, gameDisplay, alloted_time)
    return score


def gameLoop(gamerunvalue: bool, gameDisplay, alloted_time) -> int:
    """
    Runs the gameloop to display the game
    :param gamerunvalue:
    :param gameDisplay:
    :return: exit status 0 on quit or score on gameover
    """
    gameOver = gamerunvalue

    lead_x = DISPLAY_WIDTH / 2  # x and y locations for the head of the snake
    lead_y = DISPLAY_HEIGHT / 2
    lead_dx = BLOCK_SIZE
    lead_dy = 0
    direction = 'right'
    randAppleX = random.randrange(0, DISPLAY_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    randAppleY = random.randrange(0, DISPLAY_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    snakeList = []
    snakeLength = 1
    score = 1
    start_time = time.time()  # init a start time
    duration = 0

    while gameOver is not True:

        duration = time.time()  # getting the total duration
        difference = duration - start_time

        if difference >= alloted_time:
            gameOver = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction is not 'right':
                    lead_dx = -BLOCK_SIZE
                    lead_dy = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction is not 'left':
                    lead_dx = BLOCK_SIZE
                    lead_dy = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and direction is not 'down':
                    lead_dy = -BLOCK_SIZE
                    lead_dx = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction is not 'up':
                    lead_dy = BLOCK_SIZE
                    lead_dx = 0
                    direction = 'down'

        lead_x += lead_dx
        lead_y += lead_dy

        if lead_x >= DISPLAY_WIDTH or lead_x < 0 or lead_y >= DISPLAY_HEIGHT or \
                lead_y < 0:
            gameOver = True

        gameDisplay.fill(BACKGROUND)

        appleThickness = 30
        pygame.draw.rect(gameDisplay, APPLE, [randAppleX, randAppleY,
                                            appleThickness, appleThickness])

        # store the position of the front of the snake in an empty list
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        # add the position of the front of the snake to the list that holds all elements
        # of our snake
        snakeList.append(snakeHead)

        # if the size of the snake list is bigger then the length the snake is supposed to be,
        # delete the 'end' of the snake
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # check if snake collides with itself
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        for xy in snakeList:
            pygame.draw.rect(gameDisplay, SNAKE1, [xy[0], xy[1], BLOCK_SIZE, BLOCK_SIZE])

        pygame.display.update()
        if randAppleX < lead_x < randAppleX + appleThickness or lead_x + BLOCK_SIZE > randAppleX and lead_x + BLOCK_SIZE < randAppleX + appleThickness:
            if randAppleY < lead_y < randAppleY + appleThickness or lead_y + BLOCK_SIZE > randAppleY and lead_y + BLOCK_SIZE < randAppleY + appleThickness:
                randAppleX = random.randrange(0, DISPLAY_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
                randAppleY = random.randrange(0, DISPLAY_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
                snakeLength += 1
                score += 1

        clock.tick(FPS)
        
    if tkinter.messagebox.askyesno(title="GameOver", message= ("You Scored " + str(snakeLength) +"\n Do You Want to Replay")):
        singleplayer(DIFF, alloted_time)
    else:
        pygame.quit()
    return score


alloted_time = 5  # variable that changes based on the time trial selected


# top scores arranged = > [1, 1, 1]
"""
pickle_in = open("score.pickle", 'rb')
high_scores = pickle.load(pickle_in)
print(high_scores)

flag = True  # checks to see if the a score has been replaced, after 1 change disregard the for loop
for i in range(len(high_scores)):
    while flag:
        if score > high_scores[i]:  # change the highscore if at index the score is changed
            print(score)
            flag = False
"""
# sets the new highscore
# pickle_out = open("score.pickle", "wb")
# pickle.dump(high_scores, pickle_out)
# pickle_out.close()


# this resets the scores
pickle_out = open("score.pickle", "wb")
pickle.dump([1, 1, 1], pickle_out)
pickle_out.close()

# print("New highscore!:" + str(score))
