import math
import random
import pygame
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

# battleship
battleshipImg = pygame.image.load('battleship.png')
battleshipX = 368
battleshipY = 480
battleshipX_change = 0
battleshipY_change = 0

# aliens
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 12

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append((random.randint(50, 150)))
    alienX_change.append(3.0)
    alienY_change.append(40)

# laser
laserImg = pygame.image.load('laser.png')
laserX = 0.0
laserY = 480
laserX_change = 0.0
laserY_change = 10
laser_state = "ready"

# score
score_value = 0
font = pygame.font.Font('shuttleX.ttf', 32)

textX = 10
textY = 10

# game over text
game_over_font = pygame.font.Font('shuttleX.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    end_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(end_text, (200, 250))


def battleship(x, y):
    screen.blit(battleshipImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def shot_laser(x, y):
    global laser_state
    laser_state = "shot"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(alienX, alienY, laserX, laserY):
    distance = math.sqrt((math.pow(alienX - laserX, 2)) + (math.pow(alienY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether right or left press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                battleshipX_change -= 4.0
            if event.key == pygame.K_RIGHT:
                battleshipX_change = 4.0
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    laserX = battleshipX
                    shot_laser(laserX, laserY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            battleshipX_change = 0.0

    battleshipX += battleshipX_change

    if battleshipX <= 0:
        battleshipX = 0
    elif battleshipX >= 736:
        battleshipX = 736

    for i in range(num_of_aliens):

        # game over
        if alienY[i] > 440:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 3.0
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -3.0
            alienY[i] += alienY_change[i]

        collision = isCollision(alienX[i], alienY[i], laserX, laserY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "shot":
        shot_laser(laserX, laserY)
        laserY -= laserY_change

    battleship(battleshipX, battleshipY)
    show_score(textX, textY)

    pygame.display.update()
