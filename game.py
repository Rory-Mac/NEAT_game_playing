import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (0, 0, 255)
OBSTACLE_COLOR = (255, 0, 0)
MAX_FRAME_RATE = 60

#----------------------------------------------------------------------
# Initialise game features and define obstacle map
#----------------------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = pygame.Rect(SCREEN_WIDTH / 2 - (PLAYER_WIDTH / 2), SCREEN_HEIGHT / 2 - (PLAYER_HEIGHT / 2) , PLAYER_WIDTH, PLAYER_HEIGHT) 
obstacles = []

#----------------------------------------------------------------------
# This section is responsible for player movement
#----------------------------------------------------------------------
def update_player_movement(event, player_movement):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player_movement[0] = True
        elif event.key == pygame.K_DOWN:
            player_movement[1] = True
        elif event.key == pygame.K_LEFT:
            player_movement[2] = True
        elif event.key == pygame.K_RIGHT:
            player_movement[3] = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            player_movement[0] = False
        elif event.key == pygame.K_DOWN:
            player_movement[1] = False
        elif event.key == pygame.K_LEFT:
            player_movement[2] = False
        elif event.key == pygame.K_RIGHT:
            player_movement[3] = False


#----------------------------------------------------------------------
# This section is the main game loop and is responsible for managing
# the sequence of screen events and player actions
#----------------------------------------------------------------------
player_movement = [False, False, False, False] # up, down, left, right
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit(0)
        update_player_movement(event, player_movement)     
    
    # for continuous movement
    if player_movement[0] and player.y > 0:
        player.y -= 5
    if player_movement[1] and player.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player.y += 5
    if player_movement[2] and player.x > 0:
        player.x -= 5
    if player_movement[3] and player.x < SCREEN_WIDTH - PLAYER_WIDTH:
        player.x += 5

    # Set the maximum frame rate
    clock.tick(MAX_FRAME_RATE)

    # update frame buffer
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # advance frame
    pygame.display.flip()