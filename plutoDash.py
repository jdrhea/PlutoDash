import pygame
from sys import exit
import random

pygame.init()
pygame.mixer.init()

GAME_WIDTH = 640
GAME_HEIGHT = 480

pygame.init()    
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Pluto Dash')
clock = pygame.time.Clock()


# left (x), top (y), width, height
player = pygame.Rect(100, 350, 50, 50)  # Example player rectangle
ground = pygame.Rect(0, 400, GAME_WIDTH, 80)  # Example ground rectangle
# health_bar_red = pygame.Rect(170, 120, 200, 20)  # Example health bar rectangle
# health_bar_fill = pygame.Rect(170, 120, fill, 20)  # Example health bar fill rectangle


# game images
background_image = pygame.image.load("mercurybg.jpg")
player_image = pygame.image.load("player.png")
ground_image = pygame.image.load("ground.png")
spike_image = pygame.image.load("spike.png")
doublespike_image = pygame.image.load("doubleSpike.png")
blockspike_image = pygame.image.load("blockSpike.png")
applepowerup_image = pygame.image.load("apple_powerup.png")
x2jump_image = pygame.image.load("x2jump.png")
# sound effects
metal_pipe = pygame.mixer.Sound("metal-pipe.mp3")
powerup_sound = pygame.mixer.Sound("8-bit-powerup-6768.mp3")


player_mask = pygame.mask.from_surface(player_image)
spike_mask = pygame.mask.from_surface(spike_image)

# Player movement variables  
player_speedx = 5
player_speedy = 0
player_accel = 1
player_jump = True
canJump = False   
isDespawned = False 
score = 0
jump_power = 20

# obstacle variables
obstacle_images = [spike_image, doublespike_image, blockspike_image]  # List of obstacle images
obstacle_speed = 5  # Speed at which obstacles move left
obstacle_spawn_y = 355  # Y position where obstacles are drawn
  # powerups 
powerupTypes = [applepowerup_image, x2jump_image,]  # List of powerup image

# gameover
gameover = False

# Each obstacle is a dict: {'pos': x, 'img': image}
obstacles = [
    {'pos': 400, 'img': random.choice(obstacle_images), "scored": False},  # Example obstacle positions
    {'pos': 700, 'img': random.choice(obstacle_images), "scored": False},  # Example obstacle positions},
    {'pos': 1000, 'img': random.choice(obstacle_images), "scored": False},  # Example obstacle positions},


]
powerups = [
    {'type': random.choice(powerupTypes), 'pos': 500},
    {'type': random.choice(powerupTypes), 'pos': 1500},
]
# Function to draw the game elements
def draw():
    window.blit(background_image, (0, 0))  # Draw the background image
    window.blit(player_image, (player.x, player.y))  # Draw the player image at the player's position
    window.blit(ground_image, (ground.x, ground.y))  # Draw the ground image at the ground's position
    # pygame.draw.rect(window, (255, 0, 0), health_bar)  # Draw the health bar as a red rectangle
 
    text_str = str(int(score))

    text_font = pygame.font.SysFont('Comic Sans MS', 60)
    text_render = text_font.render(text_str, True, (255, 255, 255))
    window.blit(text_render, (GAME_WIDTH/2.5 , 10))  # Draw the score text at the top-left corner

# Function to move the player
def movePlayer():
    global player_speedy, player_jump, canJump
    player.y -= player_speedy
    if (player_jump == True):
        player_speedy -= player_accel

    if player.y > 350:
        player.y = 350
        player_speedy = 0
        accel = 0
        canJump = True

def gameOver():
    global gameover
    if not gameover:
        gameover_font = pygame.font.SysFont('Comic Sans MS', 60)
        gameover_text = gameover_font.render("Game Over!", True, (255, 0, 0))
        window.blit(gameover_text, (GAME_WIDTH / 2 - gameover_text.get_width() / 2, GAME_HEIGHT / 2 - gameover_text.get_height() / 2))
        pygame.display.update()
        gameover = True
        metal_pipe.play()
        # import time
        # time.sleep(3)  # Pause for 1 second to let the sound play
        # metal_pipe.stop()

def draw_obstacles(obst):
    global score, isIncrement
    for obstacle in obstacles:
        if obstacle['img'] == blockspike_image:
            obstacle_spawn_y = 320
        else:
            obstacle_spawn_y = 355
        spike_rect = window.blit(obstacle['img'], (obstacle['pos'], obstacle_spawn_y))
        if obstacle['pos'] < -50:
            obstacle['scored'] = False  # Reset scored flag when obstacle goes off-screen
            obstacle['pos'] = GAME_WIDTH + random.randint(100, 400) 
            obstacle['img'] = random.choice(obstacle_images)
        offset_x = int(obstacle['pos'] - player.x)  # Correct offset: spike_x - player_x
        offset_y = int(obstacle_spawn_y - player.y) # spike_y - player_y
        if player_mask.overlap(spike_mask, (offset_x, offset_y)):
            gameOver()
        if player.x > obstacle['pos'] and not obstacle['scored']:
            obstacle['scored'] = True
            score += 1
def draw_powerups(powerups):
    global score, jump_power
    for powerup in powerups[:]:
        powerup_rect = window.blit(powerup['type'], (powerup['pos'], 320))  # Draw the powerup at its position
        if powerup['pos'] < -50:
            powerups.remove(powerup)  # Remove the powerup if it goes off-screen
        if player.colliderect(powerup_rect):
            powerup_sound.play()
            if powerup['type'] == applepowerup_image:
                score += 2 # Increment score by 5 when player collects a powerup
            elif powerup['type'] == x2jump_image:
                jump_power = 30
                print("Jump power increased to:", jump_power)
            powerup['pos'] = powerup['pos'] + 1000
            powerup['type'] = random.choice(powerupTypes)


    # Reset all scored flags if all are True
    if all(obstacle['scored'] for obstacle in obstacles):
        for obstacle in obstacles:
            obstacle['scored'] = False

    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    for obstacle in obstacles[:]:
        obstacle['pos'] -= obstacle_speed  # Move left by 5 pixels per frame

    for powerup in powerups[:]:
        powerup['pos'] -= obstacle_speed  # Move left by 5 pixels per frame

    keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     player.x -= player_speedx  # Move left
    # elif keys[pygame.K_RIGHT]:
    #     player.x += player_speedx # Move right

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and canJump == True and gameover == False:
        player_speedy = jump_power
        player.y -= player_speedy  # jump
        player_jump = True
        canJump = False
    elif gameover == True:
        player_speedx = 0
        player_speedy = 0
    # if player.colliderect(spike):
    #     gameover()
    if not gameover:
        draw()
        movePlayer()
        draw_obstacles(obstacles)
        draw_powerups(powerups)
        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS