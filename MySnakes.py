# from signal import pause
import pygame
import random
from datetime import date
from pygame import mixer

# import and init pygame
pygame.init()

# declaring some game variables
game_over = False
SCREENWIDTH = 900
SCREENHEIGHT = 500
fps = 17

# score = 0 # setting score initially as 0

# setting colors -> 
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green =(33, 224, 11)
foodCol = (252, 86, 3)
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
bgimg = pygame.image.load("snakes/snkSprites/bgSnakes.png")
bgimg = pygame.transform.scale(bgimg,(SCREENWIDTH,SCREENHEIGHT)).convert_alpha()

# creating a welcome png

welcomeImg = pygame.image.load("snakes/snkSprites/snake.png")
welcomeImg = pygame.transform.scale(welcomeImg,(SCREENWIDTH,SCREENHEIGHT)).convert_alpha()

go = pygame.image.load("snakes/snkSprites/go2.png")
go = pygame.transform.scale(go,(SCREENWIDTH,SCREENHEIGHT)).convert_alpha()
    
# importing default font from the system - > 
fontSys = pygame.font.SysFont(None,40)
fonts = pygame.font.SysFont(None,78)
pygame.display.set_caption("Snakes Game - My First Game")

def displayScore(text,color,x,y):
    font_render = fontSys.render(text,True,color)  # font-render variable to render the font on screen
    screen.blit(font_render,[x,y]) # blit the text score at co-ordinates x,y

def blitSnake(screen,color,list,size):
    for x,y in list:
        pygame.draw.rect(screen,color,[x,y,size,size])

# setting the clock for ticks per second ( fps )
clock = pygame.time.Clock()
                    
def welcomeScreeen():
    exit_game = False
    while not exit_game:
        screen.blit(welcomeImg,(0,0))
        displayScore("WELCOME TO THE SNAKES GAME",white,210,120)
        displayScore("PRESS SPACE BAR TO PLAY",white,250,160)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()

        pygame.display.update()
        clock.tick(50)

def gameOver(text,color,x,y):
    font_render = fonts.render(text,True,color)  # font-render variable to render the font on screen
    screen.blit(font_render,[x,y]) # blit the text score at co-ordinates x,y

def gameLoop():
    mixer.music.load('snakes/snkSprites/audio/loop.mp3')
    mixer.music.play()
    datetoday = date.today()
    day = datetoday.day
    month = datetoday.month
    print("Enter the player name ---> ")
    name = input()

    exit_game =False
    game_over = False
    initX = 80
    initY = 50
    vel_x = 0
    vel_y = 0
    snake_list = []
    sahil = 1
    initFoodx = random.randint(20,SCREENWIDTH / 2)
    initFoody = random.randint(20,SCREENHEIGHT/ 2)
    score = 0
    fps = 15

    while not exit_game:
      
        if game_over:
            screen.fill((0,0,0))
            gameOver("GAME OVER",white,270,120)
            gameOver("PRESS ENTER TO PLAY AGAIN",white,40,190)
            displayScore(f"{name} SCORED : "+str(score),white,319,290)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("scores.txt","a") as op:
                        op.write(f"Player {name} scored {score} on {day} of {month}\n")
                        op.write("=============================================================\n\n")
                    return 1 # returning from the function
                    # exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcomeScreeen()

        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        vel_x = 10
                        vel_y = 0

                    if event.key == pygame.K_LEFT:
                        vel_x = -10
                        vel_y = 0

                    if event.key == pygame.K_UP:
                        vel_y = -10
                        vel_x = 0

                    if event.key == pygame.K_DOWN:
                        vel_y = 10
                        vel_x = 0

            initX = initX + vel_x
            initY = initY + vel_y

            if abs(initX - initFoodx) < 12 and abs(initY - initFoody) < 12:
                mixer.init()
                pygame.mixer.music.load('snakes/snkSprites/audio/eat.mp3')
                pygame.mixer.music.play()
                score += 10 
                fps += 1
                # print("Your score is : ",score)
                initFoodx = random.randint(15,SCREENWIDTH / 2)
                initFoody = random.randint(25,SCREENHEIGHT / 2)
                sahil += 1
                
           
            # head = []
            # head.append(initX)
            # head.append(initY)
            snake_list.append([initX,initY])

            if len(snake_list) > sahil:
                del snake_list[0]

            if initX <= 0 or initX >= SCREENWIDTH or initY < 0  or initY >= SCREENHEIGHT - 3:
                game_over = True
                pygame.mixer.music.load('snakes/snkSprites/audio/death.mp3')
                pygame.mixer.music.play()
            
            if [initX,initY] in snake_list[:-1]:  # this means if head in rest of the list except last element
                game_over = True
                pygame.mixer.music.load('snakes/snkSprites/audio/death.mp3')
                pygame.mixer.music.play()

            # screen.fill((233,210,229))
            screen.blit(bgimg,(0,0))
            displayScore("Current score : "+str(score),red,8,8)
            displayScore("Player Name : "+name,black,550,8)
            pygame.draw.rect(screen,black,[initX,initY,14,14]) # creating snake
            pygame.draw.rect(screen,red,[initFoodx,initFoody,14,14]) # creating the food
            blitSnake(screen,black,snake_list,14)
            
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

if __name__ == "__main__":
   welcomeScreeen()