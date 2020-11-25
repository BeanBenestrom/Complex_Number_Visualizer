import pygame, sys, os, socket, threading, json
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

def add_ip_port():
    while True:
        _ip = input("ip>")
        _port = input("port>")
        if ip == "": 
            print("IP cannot be blank\n")
        else:
            try:
                port = int(port)
                if 0 <= port <= 65535:
                    print(f"\n---IP:    {ip}")
                    print(f"---PORT:  {port}\n")
                    break
                else:
                    print("Port must be between 0-65535\n")
            except ValueError:
                print("Port should only be a number\n")
    return _ip, _port


def connect_to_server(_ip, _port):
    global socketCon, tries, maxTries
    try:
        socketCon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketCon.connect((_ip, _port))
        return True
    except:
        tries += 1
        if tries >= maxTries:
            tries = 0
            print(redL + f"\nERROR: Could not connect to server after {maxTries} tries!" + white)
            print("\nPossibly the IP or the port is wrong.\n" + white)
            return False
        print(red + f"ERROR: Could not connect to server!\n       Retrying...({tries})" + white)
        time.sleep(0.5)
        create_socket()


def server_options():
    global option, ip, port
    while True:
        try:
            with open("options.json") as f:
                if f[0]["ip"] != "" and f[0]["port"] != 0:
                    ip, port = f[0]["ip"], f[0]["port"]
                print(f"USED IP, PORT: {ip, port}\n1 - Join Server\n2 - Create Server\n3 - Change ip/port\n4 - Back\n") 
                option = int(input(">"))

                # Join server
                if option == 1:
                    _ip, _port = add_ip_port()
                    if connect_to_server(_ip, _port): 
                        return True

                # Create server
                elif option == 2:
                    if server.create_socket(ip, port):
                        if connect_to_server(ip, port):
                            threading.Thread(target=server.start).start()
                            return True

                # Change ip and port
                elif option == 3:
                    _ip, _port = add_ip_port()
                    with open("options.json", "w") as f:
                        json.dump([{"ip" : _ip, "port" : _port}], f)
                else:
                    print("Please type one of the options")
        except ValueError: 
            print("Please type a number\n")
        except: 
            # Check if .json exsists
            print(redL + "ERROR: Error while loading options.json. Make sure options.json is not corrupted" + white)
            return False


def new_info():
    global info, porsion, loaded, bufferSize, headerSize
    while True:
        length = int(socketCon.recv(headerSize))
        data = bytes("", "utf-8")
        while length > 0:
            data += socketCon.recv(bufferSize); length -= bufferSize
        d = pickle.loads(data)
        if d[0]: info, porsion = d[1]
        else: print(colors.get(d[2]) + d[1] + white)    
        loaded = True


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
            threading.Thread(target=engine.start).start(); break
        elif option == 1:
            if server_options(): break
        else:
            print("Choose 1 or 2\n")
    except ValueError: 
        print("Answer with a number\n")


# Variables ------------------------------------------------------------------------------------------------------------------------- #
#                                     240
pos = [0, 0, 0]; rot = [0, 0]; zoom = 400; vel = 0.1

ip, port = socket.gethostbyname(socket.gethostname()), 55555
maxTries = 3
headerSize = 7
bufferSize = 32

w, h = 1000, 1000; fps = 120; maxArea = 1000; porsion = -1

cx, cy = w//2, h//2; mX_temp, mY_temp = 0, 0; tries = 0; loaded = True; info = ()
pygame.display.set_caption("CGV - Complex Graph Visualizer - 1.2.5")
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
            if option == 2: server.stop()
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
        if option == 2: server.stop()
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
    elif loaded:
        loaded = False
        d = pickle.dumps([pos, rot])
        serverC.send(bytes(f"{len(d):<{headerSize}}", "utf-8") + d)
    rotate(mX, mY); move(key); render()
