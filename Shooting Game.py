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

# Load and scale images
player_img = pygame.image.load('Images/Player.png')  # Replace with your image path
player_img = pygame.transform.scale(player_img, (64, 64))  # Scale to desired size
player_x = 370
player_y = 480
player_x_change = 0

enemy_img = pygame.image.load('Images/UFO.png')  # Replace with your image path
enemy_img = pygame.transform.scale(enemy_img, (64, 64))  # Scale to desired size

num_of_enemies = 6
enemies = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

for i in range(num_of_enemies):
    enemies.append(enemy_img)
    enemy_x.append(random.randint(0, screen_width - 64))
    enemy_y.append(random.randint(-300, -64))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemies[i], (x, y))

def fire_bullet(x, y):
    global bullet_state, bullet_x, bullet_y
    bullet_state = "fire"
    bullet_x = x
    bullet_y = y

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < 27

# Initial bullet state and position
bullet_state = "ready"  # "ready" - You can't see the bullet on the screen, "fire" - The bullet is currently moving
bullet_x = 0
bullet_y = 480
bullet_y_change = 5  # Adjust bullet speed

# Game Loop
running = True
while running:

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
                    bullet_x = player_x + 16  # Adjust bullet starting position
                    bullet_y = player_y + 10  # Adjust bullet starting position
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
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= screen_width - 64:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            enemy_x[i] = random.randint(0, screen_width - 64)
            enemy_y[i] = random.randint(-300, -64)

        enemy(enemy_x[i], enemy_y[i], i)

        # Check for game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000  # Move all enemies off screen
            game_over_text()
            break

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        pygame.draw.rect(screen, (255, 0, 0), (bullet_x, bullet_y, 15, 15))  # Larger rectangle for bullet
        bullet_y -= bullet_y_change

    player(player_x, player_y)

    pygame.display.update()

pygame.quit()
