import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up game constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
BALL_RADIUS = 10
MAX_BALLS = 4
WINNING_SCORE = 30
FPS = 60

# Set up colors
DARK_NAVY = (0, 0, 50)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Create the paddles
player1_paddle = pygame.Rect(20, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 20 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize the balls
balls = [
    pygame.Rect((WIDTH - BALL_RADIUS) // 3, (HEIGHT - BALL_RADIUS) // 2, BALL_RADIUS, BALL_RADIUS),
    pygame.Rect((2 * WIDTH - BALL_RADIUS) // 3, (HEIGHT - BALL_RADIUS) // 2, BALL_RADIUS, BALL_RADIUS)
]

ball_speeds = [
    [4, 4],  # Faster ball speed for ball 1
    [-4, -4]  # Reverse direction for ball 2
]

# Set up the score
score_player1 = 0
score_player2 = 0
font = pygame.font.Font(None, 36)

# Set up the clock
clock = pygame.time.Clock()

# Set up the timer for adding a new ball
new_ball_timer = pygame.time.get_ticks() + 10000  # 10000 milliseconds (10 seconds)

# Winner screen flag
winner_screen = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move the player1 paddle with 'W' and 'S' keys
    player1_paddle.y += (keys[pygame.K_s] - keys[pygame.K_w]) * 7  # Faster paddle speed

    # Move the player2 paddle with arrow keys
    player2_paddle.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 7  # Faster paddle speed

    # Keep the paddles within the screen boundaries
    player1_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, player1_paddle.y))
    player2_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, player2_paddle.y))

    # Move the balls
    for i in range(len(balls)):
        balls[i].x += ball_speeds[i][0]
        balls[i].y += ball_speeds[i][1]

        # Check for collisions with paddles
        if balls[i].colliderect(player1_paddle) or balls[i].colliderect(player2_paddle):
            ball_speeds[i][0] = -ball_speeds[i][0]

        # Check if the ball has hit the top or bottom of the screen
        if balls[i].y <= 0 or balls[i].y >= HEIGHT - BALL_RADIUS:
            ball_speeds[i][1] = -ball_speeds[i][1]

        # Check if the ball has passed the paddles and scored a point
        if balls[i].x < 0:
            balls[i].x = (WIDTH - BALL_RADIUS) // 2
            balls[i].y = (HEIGHT - BALL_RADIUS) // 2
            ball_speeds[i][0] = random.choice([-4, 4])
            ball_speeds[i][1] = random.choice([-4, 4])
            score_player2 += 1

        if balls[i].x > WIDTH:
            balls[i].x = (WIDTH - BALL_RADIUS) // 2
            balls[i].y = (HEIGHT - BALL_RADIUS) // 2
            ball_speeds[i][0] = random.choice([-4, 4])
            ball_speeds[i][1] = random.choice([-4, 4])
            score_player1 += 1

    # Check if it's time to add a new ball
    current_time = pygame.time.get_ticks()
    if len(balls) < MAX_BALLS and current_time > new_ball_timer:
        balls.append(pygame.Rect((WIDTH - BALL_RADIUS) // 2, (HEIGHT - BALL_RADIUS) // 2, BALL_RADIUS, BALL_RADIUS))
        ball_speeds.append([random.choice([-4, 4]), random.choice([-4, 4])])
        new_ball_timer = current_time + 10000  # Set the timer for the next ball (10 seconds)

    # Check for a winner
    if score_player1 >= WINNING_SCORE or score_player2 >= WINNING_SCORE:
        winner_screen = True
        winner_time = current_time

    # Draw everything
    screen.fill(DARK_NAVY)

    # Draw the grey line down the middle
    pygame.draw.line(screen, GREY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    pygame.draw.rect(screen, WHITE, player1_paddle)
    pygame.draw.rect(screen, WHITE, player2_paddle)

    for ball in balls:
        pygame.draw.ellipse(screen, WHITE, ball)

    # Draw the score
    score_text = font.render(f"{score_player1} - {score_player2}", True, WHITE)
    screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, 20))

    # Draw the winner screen if applicable
    if winner_screen:
        winner_text = font.render("Player 1 Wins!" if score_player1 >= WINNING_SCORE else "Player 2 Wins!", True, WHITE)
        screen.blit(winner_text, ((WIDTH - winner_text.get_width()) // 2, HEIGHT // 2))

        # End the game after 5 seconds
        if pygame.time.get_ticks() - winner_time > 5000:
            pygame.quit()
            sys.exit()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
