# ALIEN AND WALL COLLISION FIX

import random
import math
import pygame
from pygame.locals import *

# initialize pygame
pygame.init()

# Create a screen
WIDTH = 896
HEIGHT = 768
win = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)

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
    (9, 0), (9, 3), (9, 4), (9, 5), (9, 7), (9, 11),
    (10, 0), (10, 4), (10, 11),
    (11, 0), (11, 1), (11, 2), (11, 7), (11, 9), (11, 11),
    (12, 0), (12, 5), (12, 6), (12, 7), (12, 11),
    (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 10), (13, 11)
]
num_of_walls = len(wallCord)

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
alienX = list(map(lambda x: x*64, [1, 2, 2, 4, 5, 6, 7, 9, 10, 12]))
alienY = list(map(lambda x: x*64, [6, 3, 10, 7, 4, 8, 5, 2, 6, 10]))
vel = 3
alienX_change = []
alienY_change = []
directions = ["left", "up", "down", "right", "stop"]
alienDirection = []
alien_move_count = 0
num_of_alien = 10
entry = []

for i in range(num_of_alien):
    alienImg.append(pygame.transform.scale(pygame.image.load('alien_b.png'), [50, 50]))
    alienX_change.append(0)
    alienY_change.append(0)
    alienDirection.append(random.choice(directions[:4]))
    entry.append(False)


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


# game loop
running = True
while running:
    win.fill((25, 25, 25))
    alien_move_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

        # change direction in every 10 moves
        if alien_move_count == 299:
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

    pygame.display.update()

pygame.quit()