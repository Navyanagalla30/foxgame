import pygame
from pygame import mixer
import math
import random
# initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# Background
background =pygame.image.load("bg41.png")
# Background sound
mixer.music.load("251284__djgriffin__135-ravey-game-loop-6.wav")
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("chick (1).png")
pygame.display.set_icon(icon)
# Player
playerImg =pygame.image.load("man (1).png")
playerX = 370
playerY = 480
playerX_change = 0
# Enemy
enemyImg= []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("fox (1).png"))
    enemyX.append(random.randint(0 ,736))
    enemyY.append(random.randint(50 ,150))
    enemyX_change.append(4)
    enemyY_change.append(40)
# Bullet
#Read - you cannot see the bullet on the screen
#fire - the bullet is currently moving
bulletImg = pygame.image.load("water-balloons.png")
#sample = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True ,(255,255,255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text = over_font.render("GAME OVER : ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y + 20))
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX- bulletX, 2) + math.pow(enemyY- bulletY, 2))
    if distance <27:
        return True
    else :
        return False
# Game loop
running= True
while running:
    # RGB -Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # If Keystroke is pressed check wheather its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bullet_Sound = mixer.Sound("421184__inspectorj__water-pouring-a.wav")
                bullet_Sound.play()
                # get the current x coordinate of the spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
            playerX_change = 0
    # 5 = 5 + -0.1 =4.9
    # 5 = 5 + 0.1 =5.1
    #checking for boundarie of spaceship so it doesn't go out of bound
    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    elif playerX>=736:
        playerX = 736
    # Enemy Movement
    for i in range(num_of_enemies):
        # Gameover
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("646568__ryanz-official__watersplash.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -=bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()