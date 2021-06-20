#! /usr/bin/env_python
import pygame, sys

# from pygame.local import *

pygame.init()

win = pygame.display.set_mode((400, 300))

pygame.display.set_caption("Game Zone")

RED = (10, 10, 10)
clock = pygame.time.Clock()

counter = 0
sprites = []
up_sprites = []
down_sprites = []
back_sprites = []

sheet = pygame.image.load("dynamic_player.png").convert_alpha()
down_sheet = pygame.transform.rotate(sheet, -90)
up_sheet = pygame.transform.rotate(sheet, 90)
back_sheet = pygame.transform.rotate(sheet, -180)

x = 0
y = 0
x_change = 0
y_change = 0

for i in range(2):
    sprites.append(sheet.subsurface(i * 64, 0, 64, 64))
    up_sprites.append(up_sheet.subsurface(0, i * 64, 64, 64))
    down_sprites.append(down_sheet.subsurface(0, i * 64, 64, 64))
    back_sprites.append(back_sheet.subsurface(i * 64, 0, 64, 64))

img = sprites
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -10
                y_change = 0
                img = back_sprites
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = -10
                img = up_sprites
            if event.key == pygame.K_RIGHT:
                x_change = 10
                y_change = 0
                img = sprites
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = 10
                img = down_sprites
        if event.type == pygame.KEYUP:
            x_change = 0
            y_change = 0

    pygame.time.wait(250)
    px = x
    py = y

    win.fill(RED)
    x += x_change
    y += y_change
    win.blit(img[counter], (x, y))
    if px is not x or py is not y:
        counter = (counter + 1) % 2

    pygame.draw.rect(win, (255, 0, 0), (100, 100, 128, 100), 2)
    pygame.draw.rect(win, (255, 0, 0), (x, y, 64, 64), 2)

    # set player and barrier rectangle
    playerRect = pygame.Rect(x, y, *img[counter].get_size())
    barrierRect = pygame.Rect(100, 100, 128, 100)

    # check for collision
    if playerRect.colliderect(barrierRect):
        # reset position
        x, y = px, py

    pygame.display.update()
