import random

import pygame

# initialize pygame
pygame.init()

# Create a screen
WIDTH = 768
HEIGHT = 640
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Tab name and icon
pygame.display.set_caption("Alien Boom")
icon = pygame.image.load('alien_g.png')
pygame.display.set_icon(icon)

# Walls
wallImg = pygame.image.load('wall.png')
wallX = []
wallY = []
wallCord = [
    (0, 1), (0, 4), (0, 7), (0, 8),
    (1, 1), (1, 3), (1, 4),
    (2, 6), (2, 7), (2, 9),
    (3, 3), (3, 4), (3, 7), (3, 9),
    (4, 0), (4, 1), (4, 4), (4, 9),
    (5, 0), (5, 4), (5, 5),
    (6, 0), (6, 1), (6, 8),
    (7, 3), (7, 7), (7, 9),
    (8, 0), (8, 2), (8, 3), (8, 4), (8, 6),
    (9, 0), (9, 3),
    (10, 0), (10, 1), (10, 6), (10, 8),
    (11, 0), (11, 3), (11, 4), (11, 5), (11, 6), (11, 9)
]
num_of_walls = 44

for cord in wallCord:
    wallX.append(cord[0] * 64)
    wallY.append(cord[1] * 64)


def wall(x, y):
    win.blit(wallImg, (x, y))


def wall_mask(img):
    return pygame.mask.from_surface(img)


# Alien
alienImg = pygame.transform.scale(pygame.image.load('alien_g.png'), [50, 50])
alienX = random.randint(0, 718)
alienY = random.randint(0, 576)
vel = 0.3
alienX_change = 0
alienY_change = 0
directions = ["left", "up", "down", "right", "stop"]
alienDirection = "left"
alien_move_count = 0
entry = False


# draw alien function
def draw_alien(x, y):
    win.blit(alienImg, (x, y))


# Collision Boolean function
def collision(alienImg, wallImg, ax, ay, wx, wy):
    alien_mask = pygame.mask.from_surface(alienImg)
    offset = (round(wx - ax), round(wy - ay))
    collide = alien_mask.overlap(wall_mask(wallImg), offset)

    if collide:
        return True

    return False


# game loop
running = True
while running:
    win.fill((25, 25, 25))
    alien_move_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # set alien movement in according to direction
    if alienDirection == "left":
        alienX_change = -vel
        alienY_change = 0
    if alienDirection == "down":
        alienX_change = 0
        alienY_change = vel
    if alienDirection == "right":
        alienX_change = vel
        alienY_change = 0
    if alienDirection == "up":
        alienX_change = 0
        alienY_change = -vel
    if alienDirection == "stop":
        alienX_change = 0
        alienY_change = 0

    # setting borders
    if alienX <= 5:
        alienDirection = "up"
        alienX += vel
    if alienY <= 5:
        alienY += vel
        alienDirection = "right"
    if alienX >= WIDTH - 62:
        alienX -= vel
        alienDirection = "down"
    if alienY >= HEIGHT - 62:
        alienY -= vel
        alienDirection = "left"

    # change direction in every 10 moves
    if alien_move_count == 2999:
        alienDirection = random.choice(directions)
        alien_move_count = 0

    # move and draw alien
    alienY += alienY_change
    alienX += alienX_change
    draw_alien(alienX, alienY)

    for i in range(num_of_walls):
        wall(wallX[i], wallY[i])

        # if collide then change position
        collide = collision(alienImg, wallImg, alienX, alienY, wallX[i], wallY[i])

        if collide:
            if alienDirection == "left":
                alienX += 5
                alienDirection = random.choice(["up", "down", "right"])
                continue
            elif alienDirection == "up":
                alienY += 5
                alienDirection = random.choice(["right", "left", "down"])
                continue
            elif alienDirection == "right":
                alienX -= 5
                alienDirection = random.choice(["down", "left", "up"])
                continue
            elif alienDirection == "down":
                alienY -= 5
                alienDirection = random.choice(["right", "left", "up"])
                continue

    pygame.display.update()

pygame.quit()
