import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Shooting Game")

# Player
player_img = pygame.image.load('player.png')  # Replace with your image path
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = pygame.image.load('enemy.png')  # Replace with your image path
enemy_x = random.randint(0, screen_width - 64)
enemy_y = random.randint(50, 150)
enemy_x_change = 0.3
enemy_y_change = 40

# Bullet
bullet_img = pygame.image.load('bullet.png')  # Replace with your image path
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 1
bullet_state = "ready"  # "ready" - You can't see the bullet on the screen, "fire" - The bullet is currently moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < 27

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - 64:
        player_x = screen_width - 64

    # Enemy movement
    enemy_x += enemy_x_change
    if enemy_x <= 0:
        enemy_x_change = 0.3
        enemy_y += enemy_y_change
    elif enemy_x >= screen_width - 64:
        enemy_x_change = -0.3
        enemy_y += enemy_y_change

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Collision
    collision = is_collision(enemy_x, enemy_y, bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score_value += 1
        enemy_x = random.randint(0, screen_width - 64)
        enemy_y = random.randint(50, 150)

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score(text_x, text_y)

    # Check for game over
    if enemy_y > 440:
        for j in range(enemy_y, screen_height):
            enemy_y += 10
        game_over_text()
        break

    pygame.display.update()
