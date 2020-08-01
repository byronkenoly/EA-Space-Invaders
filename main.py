import pygame
import random
import math
from pygame import mixer
#from threading import Timer
#from time import sleep

#Spicy P

def main():
    # initialize pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # background
    background = pygame.image.load('./images/ea3.jpg')

    #background music
    mixer.music.load('./audio/futsalshuffle2020.mp3')
    mixer.music.play(-1)

    # title and icon
    pygame.display.set_caption("Eternal Atake")
    icon = pygame.image.load('./images/spaceship.png')
    pygame.display.set_icon(icon)

    # player
    player_image = pygame.image.load('./images/spaceinvaders.png')
    playerX = 370
    playerY = 480
    playerX_change = 0
    playerY_change = 0

    # enemy
    enemy_image = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    #global num_of_enemies
    num_of_enemies = 10

    '''
    def increase_enemies():
        global num_of_enemies
        num_of_enemies += 1
    
    def speed_increase():
        Timer(5.0, speed_increase).start()
        speed = 2
        del enemyX_change[0]
        enemyX_change.append(speed + 4)
    '''

    for i in range(num_of_enemies):
        enemy_image.append(pygame.image.load('./images/alien.png'))
        enemyX.append(random.randint(0, 751))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(2)
        #speed_increase()
        enemyY_change.append(40)

    # bullet
    bullet_image = pygame.image.load('./images/bullet.png')
    bulletX = 0
    bulletY = 3000
    bulletX_change = 0
    bulletY_change = 3
    bullet_state = "ready"

    #score
    score_value = 0
    count_score = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    textY = 10

    # game over text
    over_font = pygame.font.Font('freesansbold.ttf', 32)

    def pause_message():
        msg = over_font.render("Game Paused. Press C to continue", True, (255, 255, 255))
        screen.blit(msg, (130, 250))

    def game_over_text():
        over_text = over_font.render("Game Over. Press R to restart", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def show_score(x, y):
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def player(x, y):
        screen.blit(player_image, (x, y))

    def enemy(x, y, i):
        screen.blit(enemy_image[i], (x, y))

    def bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bullet_image, (x + 16, y + 10))

    def is_collision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def paused():
        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

            pause_message()
            pygame.display.update()
            
    def restart():

        restart = True

        while restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                else:
                    main()
                    quit()


    # game loop
    running = True
    while running:

        # colour scheme
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its left or right
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    playerX_change = +4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        # gets current coordinate of spaceship
                        bullet_sound = mixer.Sound('./audio/laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        bulletY = 480
                        bullet(bulletX, bulletY)
                        bullet_state = "fire"
                if event.key == pygame.K_p:
                    paused()
                if event.key == pygame.K_r:
                    restart()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # boundaries
        playerX = playerX + playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        #Thread(target=enemy_num).start()

        # enemy movement
        for i in range(num_of_enemies):

            # game over
            if enemyY[i] > 470:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = +2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 751:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            # collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('./audio/explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 2
                count_score = score_value
                #print(score_value)
                enemyX[i] = random.randint(0, 751)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        '''
        if count_score == 4:
            num_of_enemies += 1
            count_score = 0
        '''

        # bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            bullet(bulletX, bulletY)
            bulletY -= bulletY_change


        player(playerX, playerY)
        show_score(textX, textY)
        #Timer(5.0, increase_enemies).start()

        pygame.display.update()

main()