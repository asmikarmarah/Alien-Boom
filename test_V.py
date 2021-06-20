import random
import math
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
wallImg = []
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
    wallImg.append(pygame.image.load('wall.png'))
    wallX.append(cord[0] * 64)
    wallY.append(cord[1] * 64)


def wall(img, x, y):
    win.blit(img, (x, y))


def wall_mask(img):
    return pygame.mask.from_surface(img)


# Alien
alienImg = []
alienX = []
alienY = []
vel = 1
alienX_change = []
alienY_change = []
directions = ["left", "up", "down", "right", "stop"]
alienDirection = []
alien_move_count = 0
num_of_alien = 10
entry = False

for i in range(num_of_alien):
    alienImg.append(pygame.transform.scale(pygame.image.load('alien_g.png'), [50, 50]))
    alienX.append(random.randint(0, 718))
    alienY.append(random.randint(64, 576))
    alienX_change.append(0)
    alienY_change.append(0)
    alienDirection.append(random.choice(directions[:4]))


# draw alien function

def draw_alien(img, x, y):
    win.blit(img, (x, y))


# Collision Boolean function
def collision(objImg, wallImg, ox, oy, wx, wy):
    obj_mask = pygame.mask.from_surface(objImg)
    offset = (round(wx - ox), round(wy - oy))
    collide = obj_mask.overlap(wall_mask(wallImg), offset)

    if collide:
        return True

    return False


def math_collision(ax, ay, wx, wy):
    distance = math.sqrt(math.pow(ax - wx, 2) + math.pow(ay - wy, 2))
    if distance < 46:
        return True

    return False


# Player
# subsurface list
sprites = []
flip_sprites = []

# player image
sheet = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), (100, 50))
flip_sheet = pygame.transform.rotate(sheet, -90)

# cords of player
x = 0
y = 0
x_change = 0
y_change = 0
player_animation = 0
counter = 0

# appending subsurface in list
for i in range(2):
    sprites.append(sheet.subsurface(i * 50, 0, 50, 50))
    flip_sprites.append(flip_sheet.subsurface(0, i * 50, 50, 50))

# for change img on rotation
img = sprites

# game loop
running = True
while running:
    win.fill((25, 25, 25))
    alien_move_count += 1
    player_animation += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -10
                y_change = 0
                img = sprites
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = -10
                img = flip_sprites
            if event.key == pygame.K_RIGHT:
                x_change = 10
                y_change = 0
                img = sprites
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = 10
                img = flip_sprites
        if event.type == pygame.KEYUP:
            x_change = 0
            y_change = 0

    for i in range(num_of_alien):
        # set alien movement in according to direction
        if alienDirection[i] == "left":
            alienX_change[i] = -vel
            alienY_change[i] = 0
        if alienDirection[i] == "down":
            alienX_change[i] = 0
            alienY_change[i] = vel
        if alienDirection[i] == "right":
            alienX_change[i] = vel
            alienY_change[i] = 0
        if alienDirection[i] == "up":
            alienX_change[i] = 0
            alienY_change[i] = -vel
        if alienDirection[i] == "stop":
            alienX_change[i] = 0
            alienY_change[i] = 0

        # setting borders
        if alienX[i] <= 5:
            alienDirection[i] = "up"
            alienX[i] += vel
        if alienY[i] <= 5:
            alienY[i] += vel
            alienDirection[i] = "right"
        if alienX[i] >= WIDTH - 59:
            alienX[i] -= vel
            alienDirection[i] = "down"
        if alienY[i] >= HEIGHT - 59:
            alienY[i] -= vel
            alienDirection[i] = "left"

        # change direction in every 10 moves
        if alien_move_count == 2999:
            alienDirection[i] = random.choice(directions)
            alien_move_count = 0

        # move and draw alien
        alienY[i] += alienY_change[i]
        alienX[i] += alienX_change[i]
        draw_alien(alienImg[i], alienX[i], alienY[i])

        for j in range(num_of_walls):
            wall(wallImg[j], wallX[j], wallY[j])

            # if collide then change position
            collide = collision(alienImg[i], wallImg[j], alienX[i], alienY[i], wallX[j], wallY[j])

            entry_collision = math_collision(alienX[i], alienY[i], wallX[j], wallY[j])
            if entry_collision:
                alienX[i] = random.randint(0, 718)
                alienY[i] = random.randint(64, 576)

            if collide:
                if alienDirection[i] == "left":
                    alienX[i] += 5
                    alienDirection[i] = random.choice(["up", "down", "right"])
                    continue
                elif alienDirection[i] == "up":
                    alienY[i] += 5
                    alienDirection[i] = random.choice(["right", "left", "down"])
                    continue
                elif alienDirection[i] == "right":
                    alienX[i] -= 5
                    alienDirection[i] = random.choice(["down", "left", "up"])
                    continue
                elif alienDirection[i] == "down":
                    alienY[i] -= 5
                    alienDirection[i] = random.choice(["right", "left", "up"])
                    continue
            player_border = collision(img[counter], wallImg[j], x, y, wallX[j], wallY[j])
            if player_border:
                x += (- 1 * x_change * 1.2)
                y += (- 1 * y_change * 1.2)
                x_change = 0
                y_change = 0

    # player movement
    x += x_change
    y += y_change
    win.blit(img[counter], (x, y))
    if player_animation == 5:
        counter = (counter + 1) % 2
        player_animation = 0

    # player borders
    if x < 0:
        x = 15
    if x > WIDTH-50:
        x = WIDTH - 62
    if y < 0:
        y = 15
    if y > HEIGHT-50:
        y = HEIGHT - 62
    pygame.display.update()

pygame.quit()
