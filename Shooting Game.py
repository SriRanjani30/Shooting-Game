import pygame
import sys
import random

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
    bullets_to_remove = []
    enemies_to_remove = []

    for i, bullet in enumerate(bullets):
        bullet_x, bullet_y = bullet
        bullet_y -= bullet_speed
        bullets[i] = (bullet_x, bullet_y)

        # Remove bullets that are off-screen
        if bullet_y < 0:
            bullets_to_remove.append(bullet)

        # Collision detection with enemies
        for j, enemy in enumerate(enemies):
            enemy_x, enemy_y = enemy
            if (enemy_x < bullet_x < enemy_x + enemy_size) and (enemy_y < bullet_y < enemy_y + enemy_size):
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(j)

    # Remove bullets and enemies after collision detection loop
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    for index in sorted(enemies_to_remove, reverse=True):
        enemies.pop(index)

    # Generate enemies
    if len(enemies) < 5:
        enemy_x = random.randint(0, screen_width - enemy_size)
        enemy_y = -enemy_size
        enemies.append((enemy_x, enemy_y))

    # Update enemies
    for i, enemy in enumerate(enemies):
        enemy_x, enemy_y = enemy
        enemy_y += enemy_speed
        enemies[i] = (enemy_x, enemy_y)

        # Remove enemies that are off-screen
        if enemy_y > screen_height:
            enemies.pop(i)

    # Draw player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_size, bullet_size))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, (enemy[0], enemy[1], enemy_size, enemy_size))

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
