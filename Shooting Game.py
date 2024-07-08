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

initial_num_of_enemies = 1  # Start with only 1 enemy
initial_enemy_speed = 0.05  # Slower initial speed

# Bullet properties
bullet_width = 5
bullet_height = 20
bullet_color = (255, 0, 0)
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 1
bullet_state = "ready"  # "ready" - You can't see the bullet on the screen, "fire" - The bullet is currently moving

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Life points
life_points = 5

# Score
score_value = 0

def show_life_points(x, y):
    life_points_text = font.render("Life Points: " + str(life_points), True, (255, 255, 255))
    screen.blit(life_points_text, (x, y))

def show_score(x, y):
    score_text = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (250, 350))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemies[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    pygame.draw.rect(screen, bullet_color, (x + 29, y, bullet_width, bullet_height))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    return distance < 27

def increase_score():
    global score_value
    score_value += 1

def reset_game():
    global player_x, player_y, player_x_change
    global enemies, enemy_x, enemy_y, enemy_y_change, num_of_enemies, enemy_speed
    global bullet_x, bullet_y, bullet_state
    global life_points, score_value, difficulty_timer, game_over

    player_x = 370
    player_y = 480
    player_x_change = 0

    num_of_enemies = initial_num_of_enemies
    enemy_speed = initial_enemy_speed
    enemies = []
    enemy_x = []
    enemy_y = []
    enemy_y_change = []

    for i in range(num_of_enemies):
        enemies.append(enemy_img)
        enemy_x.append(random.randint(0, screen_width - 64))
        enemy_y.append(random.randint(-300, -64))
        enemy_y_change.append(enemy_speed)

    bullet_x = 0
    bullet_y = 480
    bullet_state = "ready"

    life_points = 5
    score_value = 0
    difficulty_timer = pygame.time.get_ticks()
    game_over = False

# Initialize game state
reset_game()

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key events
        if not game_over:
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
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

    # Player movement
    if not game_over:
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= screen_width - 64:
            player_x = screen_width - 64

    # Increase difficulty over time
    if pygame.time.get_ticks() - difficulty_timer > 5000 and not game_over:  # Every 5 seconds
        difficulty_timer = pygame.time.get_ticks()
        num_of_enemies += 1
        enemy_speed += 0.02  # Increase speed incrementally
        enemies.append(enemy_img)
        enemy_x.append(random.randint(0, screen_width - 64))
        enemy_y.append(random.randint(-300, -64))
        enemy_y_change.append(enemy_speed)

    # Enemy movement
    for i in range(num_of_enemies):
        if not game_over:
            enemy_y[i] += enemy_y_change[i]

            # Collision
            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                bullet_y = 480
                bullet_state = "ready"
                enemy_x[i] = random.randint(0, screen_width - 64)
                enemy_y[i] = random.randint(-300, -64)
                increase_score()

            # Reset enemy position if it moves off the bottom
            if enemy_y[i] > screen_height:
                life_points -= 1
                enemy_x[i] = random.randint(0, screen_width - 64)
                enemy_y[i] = random.randint(-300, -64)

            enemy(enemy_x[i], enemy_y[i], i)

    # Check for game over
    if life_points <= 0:
        game_over = True

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_life_points(10, 10)
    show_score(10, 50)

    if game_over:
        game_over_text()

    pygame.display.update()

pygame.quit()
