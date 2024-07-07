import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
player_size = 50
player_speed = 5
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - 2 * player_size

# Bullet settings
bullet_size = 10
bullet_speed = 10
bullet_color = (255, 0, 0)
bullets = []

# Enemy settings
enemy_size = 50
enemy_speed = 3
enemy_color = (0, 255, 0)
enemies = []

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed
            elif event.key == pygame.K_SPACE:
                # Shoot a bullet
                bullet_x = player_x + player_size // 2 - bullet_size // 2
                bullet_y = player_y
                bullets.append((bullet_x, bullet_y))

    # Update bullets
    for i, bullet in enumerate(bullets):
        bullet_x, bullet_y = bullet
        bullet_y -= bullet_speed
        bullets[i] = (bullet_x, bullet_y)

        # Remove bullets that are off-screen
        if bullet_y < 0:
            bullets.pop(i)

    # Generate enemies
    if len(enemies) < 5:
        enemy_x = pygame.time.get_ticks() % (screen_width - enemy_size)
        enemy_y = -enemy_size
        enemies.append((enemy_x, enemy_y))

    # Update enemies
    for i, enemy in enumerate(enemies):
        enemy_x, enemy_y = enemy
        enemy_y += enemy_speed
        enemies[i] = (enemy_x, enemy_y)
