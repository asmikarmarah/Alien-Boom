# player vs alien

import random
import math
import pygame
from pygame.locals import *

# initialize pygame
pygame.init()

# Create a screen
WIDTH = 896
HEIGHT = 768
win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# Tab name and icon
pygame.display.set_caption("Alien Boom")
icon = pygame.image.load('alien_g.png')
pygame.display.set_icon(icon)

# Walls
wallImg = []
wallX = []
wallY = []
wallCord = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11),
    (1, 0), (1, 2), (1, 5), (1, 8), (1, 9), (1, 11),
    (2, 0), (2, 2), (2, 4), (2, 5), (2, 11),
    (3, 0), (3, 7), (3, 8), (3, 11),
    (4, 0), (4, 4), (4, 5), (4, 8), (4, 10), (4, 11),
    (5, 0), (5, 1), (5, 2), (5, 5), (5, 10), (5, 11),
    (6, 0), (6, 1), (6, 5), (6, 6), (6, 11),
    (7, 0), (7, 1), (7, 2), (7, 9), (7, 11),
    (8, 0), (8, 4), (8, 8), (8, 10), (8, 11),
    (9, 0), (9, 3), (9, 4), (9, 5), (9, 11),
    (10, 0), (10, 4), (10, 7), (10, 11),
    (11, 0), (11, 1), (11, 2), (11, 7), (11, 9), (11, 11),
    (12, 0), (12, 5), (12, 6), (12, 7), (12, 11),
    (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 10), (13, 11)
]
num_of_walls = len(wallCord)

for cord in wallCord:
    wallImg.append(pygame.image.load('wall.png').convert_alpha())
    wallX.append(cord[0] * 64)
    wallY.append(cord[1] * 64)


def wall(img, x, y):
    win.blit(img, (x, y))


def wall_mask(img):
    return pygame.mask.from_surface(img)


# Alien
alienImg = []
alienX = list(map(lambda x: x * 64, [1, 2, 2, 4, 5, 5, 6, 7, 9, 10, 12, 12]))
alienY = list(map(lambda x: x * 64, [6, 3, 10, 7, 4, 8, 8, 5, 2, 6, 10, 10]))
vel = 2
directions = ["left", "up", "down", "right", "stop"]
alienDirection = []
alien_move_count = 0
num_of_alien = 12
playerEaten = 0

for i in range(num_of_alien):
    alienImg.append(pygame.transform.scale(pygame.image.load('alien_g.png').convert_alpha(), [50, 50]))
    alienDirection.append(random.choice(directions))


# draw alien function
def draw_alien(img, x, y):
    win.blit(img, (x, y))


# Collision Boolean function
def collision(alienImg, wallImg, ax, ay, wx, wy):
    alien_mask = pygame.mask.from_surface(alienImg)
    offset = (round(wx - ax), round(wy - ay))
    collide = alien_mask.overlap(wall_mask(wallImg), offset)

    if collide:
        return True

    return False


# Player
playerImg = pygame.image.load('static_player.png')
playerX, playerY = 64, 64
MOVE_RIGHT = 1
MOVE_LEFT = 2
MOVE_UP = 3
MOVE_DOWN = 4
playerDirection = 0
speed = 10
life = 3
# for bomb placement
face = "right"

# boom
bomb = [pygame.transform.scale(pygame.image.load('b1.png').convert_alpha(), (50, 50)),
        pygame.transform.scale(pygame.image.load('b2.png').convert_alpha(), (50, 48)),
        pygame.transform.scale(pygame.image.load('b3.png').convert_alpha(), (50, 46)),
        pygame.transform.scale(pygame.image.load('b4.png').convert_alpha(), (50, 44)),
        pygame.transform.scale(pygame.image.load('b5.png').convert_alpha(), (50, 42)),
        pygame.image.load('e1.png').convert_alpha(),
        pygame.image.load('e2.png').convert_alpha(),
        pygame.image.load('e3.png').convert_alpha(),
        pygame.image.load('e2.png').convert_alpha()]
bombX, bombY = 0, 0
fx, fy = 0, 0
bomb_counter = 0
bomb_animation = 0
fire_state = 'not ready'
isExplode = False


# draw bomb function
def draw_bomb(i, x, y):
    win.blit(bomb[i], (x, y))


clock = pygame.time.Clock()

# game loop
running = True
while running:
    win.fill((25, 25, 25))
    clock.tick(250)
    alien_move_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player controls
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                playerDirection = MOVE_LEFT
                face = "left"
            if event.key == K_RIGHT:
                playerDirection = MOVE_RIGHT
                face = "right"
            if event.key == K_UP:
                playerDirection = MOVE_UP
                face = "up"
            if event.key == K_DOWN:
                playerDirection = MOVE_DOWN
                face = "down"

            # fire bomb
            if event.key == K_SPACE and fire_state == "not ready":
                fire_state = "ready"
                if face == 'left':
                    fx, fy = playerX-50, playerY
                if face == 'up':
                    fx, fy = playerX, playerY-50
                if face == 'right':
                    fx, fy = playerX+38, playerY
                if face == 'down':
                    fx, fy = playerX, playerY+38

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                playerDirection = 0
            if event.key == K_RIGHT:
                playerDirection = 0
            if event.key == K_UP:
                playerDirection = 0
            if event.key == K_DOWN:
                playerDirection = 0

    # fire the bomb
    if fire_state == "ready":
        if bomb_counter == 0:
            bombX = fx
            bombY = fy
        elif bomb_counter == 1:
            bombX = fx
            bombY = fy + 2
        elif bomb_counter == 2:
            bombX = fx
            bombY = fy + 4
        elif bomb_counter == 3:
            bombX = fx
            bombY = fy + 6
        elif bomb_counter == 4:
            bombX = fx
            bombY = fy + 8
        elif bomb_counter == 5:
            bombX = fx - 7
            bombY = fy - 7
            isExplode = True
        elif bomb_counter == 6:
            bombX = fx - 25
            bombY = fy - 25
        elif bomb_counter == 7:
            bombX = fx - 39
            bombY = fy - 39
        elif bomb_counter == 8:
            bombX = fx - 25
            bombY = fy - 25
        draw_bomb(bomb_counter, bombX, bombY)
        bomb_animation += 1

    if bomb_animation == 5:
        bomb_counter += 1
        bomb_animation = 0

    if bomb_counter == 9:
        fire_state = "not ready"
        bombX = -500
        isExplode = False
        bomb_counter = 0

    # store current position
    px, py = playerX, playerY

    # player movement according to direction
    if playerDirection == MOVE_LEFT:
        playerX -= speed
    if playerDirection == MOVE_RIGHT:
        playerX += speed
    if playerDirection == MOVE_UP:
        playerY -= speed
    if playerDirection == MOVE_DOWN:
        playerY += speed

    for i in range(num_of_alien):
        # set alien movement in according to direction
        if alienDirection[i] == "left":
            alienX[i] -= vel
        if alienDirection[i] == "down":
            alienY[i] += vel
        if alienDirection[i] == "right":
            alienX[i] += vel
        if alienDirection[i] == "up":
            alienY[i] -= vel
        if alienDirection[i] == "stop":
            alienX[i] += 0
            alienY[i] += 0

        # change direction in every 10 moves
        if alien_move_count == 100:
            alienDirection[i] = random.choice(directions)
            alien_move_count = 0

        # move and draw alien
        draw_alien(alienImg[i], alienX[i], alienY[i])

        for j in range(num_of_walls):
            wall(wallImg[j], wallX[j], wallY[j])

            # if collide then change position
            collide = collision(alienImg[i], wallImg[j], alienX[i], alienY[i], wallX[j], wallY[j])

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

    # wall border to player
    for j in range(num_of_walls):
        collide = collision(playerImg, wallImg[j], playerX, playerY, wallX[j], wallY[j])

        # if collide then reset position
        if collide:
            playerX, playerY = px, py

    # drawing player
    win.blit(playerImg, (playerX, playerY))

    # alien under attack
    for i in range(num_of_alien):
        attack = collision(alienImg[i], bomb[bomb_counter], alienX[i], alienY[i], bombX, bombY)
        eatPlayer = collision(alienImg[i], playerImg, alienX[i], alienY[i], playerX, playerY)
        # burst on bomb
        if isExplode and attack:
            alienImg.remove(alienImg[i])
            num_of_alien = len(alienImg)
            alienX.remove(alienX[i])
            alienY.remove(alienY[i])
            alienDirection.remove(alienDirection[i])
            print(len(alienImg))
            print(len(alienX))
            print(len(alienY))
            print(len(alienDirection))
            print(num_of_alien)
            break

        # bounce back from bomb
        if attack:
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

        if eatPlayer:
            alienDirection[i] = "stop"
            playerEaten += 1
            if playerEaten == life:
                playerY = -100
                break
            playerX = 64
            playerY = 64

    playerOnBomb = collision(playerImg, bomb[bomb_counter], playerX, playerY, bombX, bombY)
    if isExplode and playerOnBomb:
        playerEaten += 1
        if playerEaten == life:
            playerY = -100
        else:
            playerX = 64
            playerY = 64
    if playerOnBomb and not isExplode:
        playerX = px
        playerY = py

    pygame.display.update()

pygame.quit()
