import math
import random
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('milky_way.jpg')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 2  # Adjust the player speed here

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_state = []  # New list to track enemy state (alive/dead)
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)  # Adjust the enemy speed here
    enemyY_change.append(20)  # Adjust the enemy speed here
    enemy_state.append("alive")  # Initialize all enemies as alive

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4  # Adjust the bullet speed here
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def victory_text():
    victory_text = over_font.render("You have Slayed All the Monsters", True, (255, 255, 255))
    screen.blit(victory_text, (50, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    if enemy_state[i] == "alive":
        screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Mute/Unmute
mute = False

# Function to check if all enemies are dead
def all_enemies_dead():
    return all(enemy == "dead" for enemy in enemy_state)

# ... (Previous code remains unchanged)

# Victory text
victory_font = pygame.font.Font('freesansbold.ttf', 36)
victory_text = None  # Initialize victory text

def display_victory_text():
    victory_text = victory_font.render("You have Slayed All the Monsters", True, (255, 255, 255))
    screen.blit(victory_text, (100, 250))

# Game Loop
running = True
victory = False  # Initialize the victory state

while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2  # Adjust the player speed here
            if event.key == pygame.K_RIGHT:
                playerX_change = 2  # Adjust the player speed here
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    if not mute:
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_m:  # M key to mute/unmute
                mute = not mute
                if mute:
                    pygame.mixer.music.pause()  # Pause background music
                else:
                    pygame.mixer.music.unpause()  # Unpause background music

    # Update player position
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement and Collision
    for i in range(num_of_enemies):
        if enemy_state[i] == "alive":
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 1  # Adjust the enemy speed here
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1  # Adjust the enemy speed here
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                if not mute:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemy_state[i] = "dead"  # Mark the enemy as dead

            # Display the enemy here inside the loop
            enemy(enemyX[i], enemyY[i], i)

    # Check if all enemies are dead
    if not any(enemy == "alive" for enemy in enemy_state) and not victory:
        victory = True
        # Initialize and display victory text once
        display_victory_text()

    # Display the victory text if victory is True
    if victory:
        display_victory_text()

    # ... (Rest of the code remains unchanged)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Display player and score
    player(playerX, playerY)
    show_score(textX, textY)

    # Update the display
    pygame.display.update()

# ... (Rest of the code remains unchanged)

