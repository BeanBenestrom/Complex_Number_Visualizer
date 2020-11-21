import pygame, sys, os, socket, threading
import colorama as color
import numpy as np
import server, engine
from math import *


pygame.init()
color.init()


# Colors ------------------------------------------------------------------------------------------------------------------------------ #

green = color.Fore.GREEN
white = color.Fore.WHITE
red = color.Fore.RED
redL = color.Fore.LIGHTRED_EX
yellow = color.Fore.LIGHTYELLOW_EX


# Socket functions -------------------------------------------------------------------------------------------------------------------- #

# pass


# User functions ---------------------------------------------------------------------------------------------------------------------- #

def rotate(mX, mY):
    rot[0] += mX*pi*0.0008
    rot[1] += mY*pi*0.0008


def move(key):
    global pos, vel, rot
    dirPos = np.array([0., 0., 0.])
    temp_vel = vel
    if key[pygame.K_LSHIFT]: temp_vel *= 5
    if key[pygame.K_w]: dirPos += rotateXZ(rotateYZ([0, 0, temp_vel], -1), -1)
    if key[pygame.K_a]: dirPos += rotateXZ([-temp_vel, 0, 0], -1)
    if key[pygame.K_s]: dirPos += rotateXZ(rotateYZ([0, 0, -temp_vel], -1), -1)
    if key[pygame.K_d]: dirPos += rotateXZ([temp_vel, 0, 0], -1)

    pos += dirPos


# Rotate functions -------------------------------------------------------------------------------------------------------------------- #

def rotateXZ(_vector, rev=1):
    global rot
    x, y, z = _vector; _rot = rot[0]*rev
    return (x*cos(_rot) - z*sin(_rot), y, x*sin(_rot) + z*cos(_rot))


def rotateYZ(_vector, rev=1):
    global rot
    x, y, z = _vector; _rot = -rot[1]*rev
    return (x, z*sin(_rot) + y*cos(_rot), z*cos(_rot) - y*sin(_rot))


# Functions -------------------------------------------------------------------------------------------------------------------------- #

def draw_dot(x, y, z):
    global pos, zoom, rot
    x -= pos[0]; y -= pos[1]; z -= pos[2]

    x, y, z = rotateYZ(rotateXZ([x, y, z]))

    if z > 0.001:
        return (int(zoom/z*x)+cx, int(zoom/z*y)+cy)
    else:
        return (None, None)


def render():
    screen.fill((0, 0, 0))
    for i in info:
        v = []
        for x, y, z in i[1]:
            dot = draw_dot(x, y, z) 
            if porsion < 0 or -porsion <= z <= porsion:
                v.append(dot)
                if i[3] and i[5] and dot[0]: 
                    pygame.draw.circle(screen, i[5], dot, 3)
            else:
                v.append((None, None))
        if i[4]: 
            for e1, e2 in i[2]:
                # print (v[e1], v[e2])
                if i[5] and v[e1][0] and v[e2][0]: pygame.draw.line(screen, i[5], v[e1], v[e2], 1)

    pygame.display.update()


# Option ---------------------------------------------------------------------------------------------------------------------------- #

while True:
    print("1 - Singleplayer\n2 - Multiplayer\n")
    try:
        option = int(input(">")) - 1

        if option == 0:
            threading.Thread(target=engine.start).start()
            break
        elif option == 1:
            print("\n1 - Join Server\n2 - Create Server\nAnything else - Back\n") 
            option = int(input(">"))

            if option == 1: 
                # Join server
                break
            elif option == 2:
                # Create server
                break
        else:
            print("Choose 1 or 2\n")
    except ValueError: 
        print("Answer with a number\n")


# Variables ------------------------------------------------------------------------------------------------------------------------- #
#                                     240
pos = [0, 0, 0]; rot = [0, 0]; zoom = 400; vel = 0.1

fps = 120; maxArea = 1000; porsion = -1; info = ()

w, h = 1000, 1000; cx, cy = w//2, h//2; mX_temp, mY_temp = 0, 0
pygame.display.set_caption("CGV - Complex Graph Visualizer - 1.1.5")
monitorInfo = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# delay = pygame.time.get_ticks()


# vectors = [[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1], [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]]
# edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]


while True:
    clock.tick(fps)
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            if option == 0: engine.stop()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        if event.type == pygame.KEYDOWN:
            pass

        # if event.type == pygame.MOUSEMOTION:

    if key[pygame.K_ESCAPE]:
        pygame.quit()
        if option == 0: engine.stop()
        sys.exit() 

    mX, mY = 0, 0
    if mouse[2]:
        mX, mY = pygame.mouse.get_pos()
        mX, mY = mX - mX_temp, mY - mY_temp
        pygame.mouse.set_pos(mX_temp, mY_temp)
    else:
        mX_temp, mY_temp = pygame.mouse.get_pos()

    # if pygame.time.get_ticks() - delay > 300:
    #     delay = pygame.time.get_ticks(); print(rot)

    if option == 0: info, porsion = engine.get_info()
    rotate(mX, mY); move(key); render()
