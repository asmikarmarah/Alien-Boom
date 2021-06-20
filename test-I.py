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

# Alien
alienImg = pygame.image.load('alien_g.png')
alienX = random.randint(0, 718)
alienY = random.randint(0, 576)
vel = 0.05
alienX_change = -vel
alienY_change = 0
alienDirection = "left"
directions = ["left", "up", "down", "right", "stop"]
alien_move_count = 0


# draw alien function
def draw_alien(x, y):
    win.blit(alienImg, (x, y))


# game loop
running = True
while running:
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
    if alienX >= WIDTH-64:
        alienX -= vel
        alienDirection = "down"
    if alienY >= HEIGHT-64:
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

    pygame.display.update()

pygame.quit()