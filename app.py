import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Space Shooter")

# FPS Control
clock = pygame.time.Clock()

# Load images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(filename, size=None):
    """Load an image safely from the static folder and resize it if needed."""
    path = os.path.join(BASE_DIR, "static", filename)
    if not os.path.exists(path):
        print(f"Error: {filename} not found!")
        pygame.quit()
        exit()
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size) if size else image

# Load assets
player_img = load_image("player.png", (64, 64))
enemy_img = load_image("enemy.png", (50, 50))
bullet_img = load_image("bullet.png", (10, 20))
background = load_image("background.jpg", (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 50)

# Game variables
player_x, player_y = WIDTH // 2 - 32, HEIGHT - 100
player_speed = 6
bullet_speed = 6
bullet_cooldown = 0  # Prevents spamming bullets

bullets = []  # Initialize bullets list
enemies = []  # Initialize enemies list
score = 0
game_over = False
level = 1  # Track level progression

# Function to reset the game
def reset_game():
    global player_x, player_y, enemies, bullets, score, game_over, level, bullet_speed, bullet_cooldown
    player_x, player_y = WIDTH // 2 - 32, HEIGHT - 100
    bullets.clear()
    enemies.clear()
    score = 0
    game_over = False
    level = 1
    bullet_speed = 6
    bullet_cooldown = 20  # Reset cooldown
    spawn_enemies()

# Function to increase difficulty
def increase_difficulty():
    global level, bullet_speed, bullet_cooldown
    level += 1
    bullet_speed += 1  # Bullets move faster
    bullet_cooldown = max(5, bullet_cooldown - 2)  # Shoot faster (min: 5)
    
    for enemy in enemies:
        enemy["speed"] += 1  # Increase enemy speed

# Function to spawn enemies
def spawn_enemies():
    global enemies
    enemies = [{"x": random.randint(50, WIDTH - 50), "y": random.randint(50, 150), "speed": random.choice([1, 2, 3])} for _ in range(6)]

# Call reset_game() after defining all global variables
reset_game()

# Function to show "Game Over" screen
def show_game_over():
    screen.fill((0, 0, 0))  # Black background
    game_over_text = font.render("Game Over! You Lost!", True, (255, 255, 255))
    restart_text = button_font.render("Restart Game", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    pygame.draw.rect(screen, (0, 128, 255), restart_rect.inflate(20, 10))  # Button background
    screen.blit(restart_text, restart_rect)
    
    pygame.display.update()

    # Wait for the player to click the restart button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    waiting = False  # Exit loop and restart game

# Main Game Loop
running = True
while running:
    clock.tick(60)  # 60 FPS
    
    if game_over:
        show_game_over()
        continue  # Skip to the next loop iteration

    # Background
    screen.blit(background, (0, 0))

    # Handle events
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
        player_x += player_speed

    # Shoot bullet with cooldown
    if keys[pygame.K_SPACE] and bullet_cooldown == 0:
        bullets.append({"x": player_x + 27, "y": player_y})
        bullet_cooldown = 20  # Reset cooldown time

    # Move bullets
    for bullet in bullets:
        bullet["y"] -= bullet_speed

    # Remove off-screen bullets
    bullets = [bullet for bullet in bullets if bullet["y"] > 0]

    # Move enemies
    for enemy in enemies:
        enemy["y"] += enemy["speed"]

        # Enemy reaches bottom (Game Over)
        if enemy["y"] > HEIGHT - 50:
            game_over = True  # Set game over state
            break

    # Check for bullet collisions
    for bullet in bullets:
        for enemy in enemies:
            if (
                enemy["x"] < bullet["x"] < enemy["x"] + 50 and
                enemy["y"] < bullet["y"] < enemy["y"] + 50
            ):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                print(f"Score: {score}")

                # Respawn enemy
                enemies.append({
                    "x": random.randint(50, WIDTH - 50),
                    "y": random.randint(50, 150),
                    "speed": random.choice([1, 2, 3]) + (level // 2)  # Increase speed with levels
                })

                # Every 5 points, increase difficulty
                if score % 5 == 0:
                    increase_difficulty()

    # Draw elements
    screen.blit(player_img, (player_x, player_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy["x"], enemy["y"]))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet["x"], bullet["y"]))

    # Display score & level
    score_text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update screen
    pygame.display.update()

    # Bullet cooldown countdown
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

pygame.quit()
