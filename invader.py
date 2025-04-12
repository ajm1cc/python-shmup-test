import pygame
import pymunk
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Pinball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Pymunk space
space = pymunk.Space()
space.gravity = (0, 300)

# Ball
ball_mass = 1
ball_radius = 10
ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
ball_body = pymunk.Body(ball_mass, ball_moment)
ball_body.position = 400, 550
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = 0.95
ball_shape.friction = 0.9
ball_shape.collision_type = 1
space.add(ball_body, ball_shape)

# Flippers
flipper_length = 80
flipper_thickness = 10

def create_flipper(position, angle, side):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Segment(body, (0, 0), (flipper_length, 0), flipper_thickness)
    shape.elasticity = 0.4
    shape.friction = 0.5
    shape.collision_type = 2
    space.add(body, shape)
    
    flipper_joint_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    flipper_joint_body.position = position
    
    joint = pymunk.PivotJoint(flipper_joint_body, body, (0,0), (0,0))
    space.add(joint)
    
    flipper_limit = pymunk.RotaryLimitJoint(flipper_joint_body, body, math.radians(angle), math.radians(angle+60))
    space.add(flipper_limit)
    
    return body

left_flipper = create_flipper((300, 550), 120, 'left')
right_flipper = create_flipper((500, 550), 60, 'right')

# Walls
def create_wall(start, end):
    shape = pymunk.Segment(space.static_body, start, end, 5)
    shape.elasticity = 0.9
    shape.friction = 0.5
    shape.collision_type = 3
    space.add(shape)

create_wall((0, 0), (WIDTH, 0))
create_wall((0, 0), (0, HEIGHT))
create_wall((WIDTH, 0), (WIDTH, HEIGHT))
create_wall((0, HEIGHT), (WIDTH, HEIGHT))

# Aliens
aliens = []

def create_alien(position):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Circle(body, 20)
    shape.collision_type = 4
    space.add(body, shape)
    aliens.append((body, shape))

for i in range(5):
    for j in range(3):
        create_alien((100 + i * 150, 100 + j * 80))

# Launcher
launcher_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
launcher_body.position = (780, 550)
launcher_shape = pymunk.Segment(launcher_body, (0, 0), (0, 50), 10)
launcher_shape.elasticity = 1.0
launcher_shape.collision_type = 5
space.add(launcher_body, launcher_shape)

# Collision handlers
def ball_alien_collision(arbiter, space, data):
    alien_shape = arbiter.shapes[1]
    space.remove(alien_shape.body, alien_shape)
    aliens[:] = [(body, shape) for body, shape in aliens if shape != alien_shape]
    return True

space.add_collision_handler(1, 4).begin = ball_alien_collision

# Game variables
score = 0
balls = 3
game_over = False
font = pygame.font.Font(None, 36)

# Helper function to convert pymunk coordinates to pygame coordinates
def to_pygame(p):
    return int(p.x), int(HEIGHT - p.y)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_flipper.angular_velocity = -20
            elif event.key == pygame.K_RIGHT:
                right_flipper.angular_velocity = 20
            elif event.key == pygame.K_SPACE and ball_body.position.y > HEIGHT:
                ball_body.position = (780, 550)
                ball_body.velocity = (0, 0)
                launcher_body.velocity = (0, -500)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_flipper.angular_velocity = 10
            elif event.key == pygame.K_RIGHT:
                right_flipper.angular_velocity = -10
            elif event.key == pygame.K_SPACE:
                launcher_body.velocity = (0, 0)

    # Clear the screen
    screen.fill(BLACK)

    # Update physics
    space.step(1/60.0)

    # Draw ball
    pygame.draw.circle(screen, WHITE, to_pygame(ball_body.position), int(ball_radius))

    # Draw flippers
    for flipper in [left_flipper, right_flipper]:
        p1 = flipper.position
        p2 = flipper.position + flipper.rotation_vector * flipper_length
        pygame.draw.line(screen, BLUE, to_pygame(p1), to_pygame(p2), 10)

    # Draw walls
    for wall in space.shapes:
        if isinstance(wall, pymunk.Segment):
            pygame.draw.line(screen, WHITE, to_pygame(wall.a), to_pygame(wall.b), 5)

    # Draw aliens
    for alien_body, alien_shape in aliens:
        pygame.draw.circle(screen, GREEN, to_pygame(alien_body.position), int(alien_shape.radius))

    # Draw launcher
    pygame.draw.line(screen, RED, to_pygame(launcher_body.position), 
                     to_pygame(launcher_body.position + (0, 50)), 10)

    # Check for lost ball
    if ball_body.position.y > HEIGHT and not game_over:
        balls -= 1
        if balls > 0:
            ball_body.position = (780, 550)
            ball_body.velocity = (0, 0)
        else:
            game_over = True

    # Update score
    score = (15 - len(aliens)) * 100

    # Draw UI
    score_text = font.render(f"Score: {score}", True, WHITE)
    balls_text = font.render(f"Balls: {balls}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(balls_text, (WIDTH - 100, 10))

    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 70, HEIGHT//2))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()