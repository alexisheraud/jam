import pygame
import sys
import random
import time

# Initialisation de Pygame
pygame.init()
WHITE = (255, 255, 255)
screen_width = 1920
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("RondoudouDash")
background_image = pygame.image.load("bg1.png").convert()

background_x = 0
background_speed = 1

# Joueur
player_image = pygame.image.load("rondoudou.png")
player_size = 50
player_width = 50
player_height = 50
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_x = screen_width // 2 - player_size // 2
player_y = (3 * screen_height) // 4 - player_size // 2
player_speed = 5
jumping = False
jump_count = 10

# Obstacles
obstacle_size = player_size
max_obstacles = 2
obstacles = []

# Chargement des images
spike_image = pygame.image.load("spike.png")
spike_image = pygame.transform.scale(spike_image, (obstacle_size, obstacle_size))

# Vitesse maximale des obstacles
max_obstacle_speed = 30

# Charger la musique
pygame.mixer.music.load('game_music.mp3')
pygame.mixer.music.play(-1)

# Score
start_time = time.time()
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()

def create_obstacle():
    random_speed = random.randint(10, max_obstacle_speed)
    spike_type = random.choice([1, 2, 3])  # 1: un spike, 2: deux spikes, 3: trois spikes
    if spike_type == 1:
        obstacle = pygame.Rect(screen_width - obstacle_size, (3 * screen_height) // 4 - obstacle_size // 2, obstacle_size, obstacle_size)
    elif spike_type == 2:
        obstacle = pygame.Rect(screen_width - obstacle_size * 2, (3 * screen_height) // 4 - obstacle_size // 2, obstacle_size * 2, obstacle_size)
    else:
        obstacle = pygame.Rect(screen_width - obstacle_size * 3, (3 * screen_height) // 4 - obstacle_size // 2, obstacle_size * 3, obstacle_size)
    obstacles.append((obstacle, random_speed, spike_type))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    if len(obstacles) == 0 and random.randint(0, 100) < 5:
        create_obstacle()

    # Déplacement obstacle
    for obstacle, speed, spike_type in obstacles:
        obstacle.x -= speed
        if obstacle.x + obstacle.width < 0:
            obstacles.remove((obstacle, speed, spike_type))

    # Déplacement de l'image de fond
    background_x -= background_speed
    if background_x <= -screen_width:
        background_x = 0

    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + screen_width, 0))

    # Afficher l'image de l'obstacle pour chaque obstacle dans la boucle d'affichage
    for obstacle, speed, spike_type in obstacles:
        if spike_type == 1:
            screen.blit(spike_image, (obstacle.x, obstacle.y))
        elif spike_type == 2:
            screen.blit(spike_image, (obstacle.x, obstacle.y))
            screen.blit(spike_image, (obstacle.x + obstacle_size, obstacle.y))
        else:
            screen.blit(spike_image, (obstacle.x, obstacle.y))
            screen.blit(spike_image, (obstacle.x + obstacle_size, obstacle.y))
            screen.blit(spike_image, (obstacle.x + obstacle_size * 2, obstacle.y))

    # Afficher le joueur
    screen.blit(player_image, (player_x, player_y))

    # Score time
    elapsed_time = time.time() - start_time
    score = int(elapsed_time * 10)
    score_display = font.render("Metro: " + str(score), True, WHITE)
    screen.blit(score_display, (20, 20))
    
    # Vérification des collisions
    for obstacle, speed, spike_type in obstacles:
        if (
            player_x < obstacle.x + obstacle.width
            and player_x + player_size > obstacle.x
            and player_y < obstacle.y + obstacle.height
            and player_y + player_size > obstacle.y
        ):
            print("Game Over - Mètres parcourus:", score)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
