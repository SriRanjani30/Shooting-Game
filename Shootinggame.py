import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen with resizable option
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

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

# Load background image
background_img = pygame.image.load('Images/Background.jpg')  # Replace with your image path
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

def show_life_points(x, y):
    life_points_text = font.render("Life Points: " + str(life_points), True, (255, 255, 255))
    screen.blit(life_points_text, (x, y))

def show_score(x, y):
    score_text = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (screen_width // 2 - 200, screen_height // 2 - 100))
    draw_buttons()

def draw_buttons():
    # Button properties
    button_width = 150
    button_height = 50
    button_border_radius = 15
    button_text_color = (255, 255, 255)
    
    # Restart button
    restart_button_rect = pygame.Rect(screen_width // 2 - button_width - 25, screen_height // 2, button_width, button_height)
    restart_button_color = (0, 200, 0)
    restart_button_hover_color = (0, 255, 0)
    restart_button_outline_color = (0, 150, 0)
    
    # Exit button
    exit_button_rect = pygame.Rect(screen_width // 2 + 25, screen_height // 2, button_width, button_height)
    exit_button_color = (200, 0, 0)
    exit_button_hover_color = (255, 0, 0)
    exit_button_outline_color = (150, 0, 0)
    
    # Mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Restart button
    if restart_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, restart_button_hover_color, restart_button_rect, border_radius=button_border_radius)
    else:
        pygame.draw.rect(screen, restart_button_color, restart_button_rect, border_radius=button_border_radius)
    pygame.draw.rect(screen, restart_button_outline_color, restart_button_rect, 3, border_radius=button_border_radius)
    restart_text = font.render("Restart", True, button_text_color)
    screen.blit(restart_text, (restart_button_rect.x + 25, restart_button_rect.y + 10))
    
    # Exit button
    if exit_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, exit_button_hover_color, exit_button_rect, border_radius=button_border_radius)
    else:
        pygame.draw.rect(screen, exit_button_color, exit_button_rect, border_radius=button_border_radius)
    pygame.draw.rect(screen, exit_button_outline_color, exit_button_rect, 3, border_radius=button_border_radius)
    exit_text = font.render("Exit", True, button_text_color)
    screen.blit(exit_text, (exit_button_rect.x + 50, exit_button_rect.y + 10))

    return restart_button_rect, exit_button_rect

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

    # Draw the background image
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle window resizing
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                restart_button_rect, exit_button_rect = draw_buttons()
                if restart_button_rect.collidepoint(mouse_pos):
                    reset_game()
                elif exit_button_rect.collidepoint(mouse_pos):
                    running = False

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

