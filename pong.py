import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
BALL_WIDTH = 10

# intialise game features
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# main game loop
running = True
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # game
    left_paddle = pygame.Rect(10, (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(SCREEN_WIDTH - (10 + PADDLE_WIDTH), (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_WIDTH, SCREEN_HEIGHT / 2 - BALL_WIDTH, BALL_WIDTH, BALL_WIDTH)

    # update frame buffer
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255,255,255), left_paddle)
    pygame.draw.rect(screen, (255,255,255), right_paddle)
    pygame.draw.rect(screen, (255,255,255), ball)

    # update the display
    clock.tick(60)
    pygame.display.flip()
pygame.quit()