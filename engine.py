# import numpy


import pygame, sys, time, threading, random, json, server
import numpy as np
from math import *


pygame.init()


# Classes ---------------------------------------------------------------------------------------------------------------------------- #

class Cam:
    def __init__(self, user):
        self.user = user
        self.pos = [0, 0, 0]
        self.rot = [0, 0]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Object:
    def __init__(self, pos, vectors, edges, useEdges=False, color=(255,255,255)):
        self.pos = np.array(pos)
        self.vectors = [np.array((x+pos[0], y+pos[1], z+pos[2])) for x, y, z in vectors]
        self.edges = None
        self.color = color
        # self.polygons = None
        # if usePolygons: self.polygons = polygons
        if useEdges: self.edges = edges


    def rotate(self, rotX=0, rotY=0, rotZ=0, axis=None):
        if axis == None: axis = self.pos
        else: axis = np.array(axis)
        rotX = rotX/360*2*pi
        rotY = rotY/360*2*pi
        rotZ = rotZ/360*2*pi
        for i in range(0, len(self.vectors)):
            self.vectors[i] = rotateXY(rotateYZ(rotateXZ(self.vectors[i]-axis, rotX), rotY), rotZ)+axis


# class Plane():
#     def __init__(self, vectors, origins, edges, useEdges=False, dotColors=[]):
#         self.vectors = vectors
#         self.origins = origins
#         self.edges = None
#         self.dotColors = dotColors
#         if useEdges: self.edges = edges


# Rotate functions ------------------------------------------------------------------------------------------------------------------- #

def rotateXZ(_vector, rot, rev=1):
    x, y, z = _vector; rot = rot*rev
    return (x*cos(rot) - z*sin(rot), y, x*sin(rot) + z*cos(rot))


def rotateYZ(_vector, rot, rev=1):
    x, y, z = _vector; rot = -rot*rev
    return (x, z*sin(rot) + y*cos(rot), z*cos(rot) - y*sin(rot))


def rotateXY(_vector, rot, rev=1):
    x, y, z = _vector; rot = rot*rev
    return (x*cos(rot) - y*sin(rot), x*sin(rot) + y*cos(rot), z)


# User functions --------------------------------------------------------------------------------------------------------------------- #

def add_cam(user):
    global cams
    cams.append(Cam(user))


def remove_cam(user):
    global cams
    for cam in cams:
        if cam.user == user: cams.remove(cam)


def update_user_info(user, pos, rot):
    global cams
    for cam in cams:
        if cam.user == user: 
            cam.pos = pos; cam.rot = rot; break


# Functions -------------------------------------------------------------------------------------------------------------------------- #


def rotate_error_cube():
    global errorCube
    rotateFps = 20
    while run:
        clock.tick(rotateFps)
        errorCube.rotate(rotX=180/rotateFps)
    

def create_plane(area, pos, values, color):
    vectors = []; edges = []; vectorOrigins = []
    area = area + 1
    for y in range(0, area):
        for x in range(0, area):
            vectorOrigins.append(pos[area*y+x]); vectors.append([pos[area*y+x][0], -values[area*y+x][0], values[area*y+x][1]])
            if area*y+x-1 >= 0 and (area*y+x) % area != 0:
                edges.append((area*y+x, area*y+x-1))
            if area*y+x-area >= 0:
                edges.append((area*y+x, area*y+x-area))
    return (0, vectors, edges, False, True, color, vectorOrigins)


# def create_line(line):
#     #      (0, vectors, False, True, color)
#     return (1, (line[0], line[1]), False, True, color)


# def create_dot(dot):
#     return (0, vectors, True, color)


def start():  
    global objs, fps, porsion
    threading.Thread(target=rotate_error_cube).start()
    while run:
        clock.tick(fps)
        temp_objs = []
        useErrorCube = False
        try:
            with open("graph_info.json") as i:
                jsonFile = json.load(i)
                useErrorCube = jsonFile[-1]["errorCube"]
                for i in range(0, len(jsonFile[0])):
                    if jsonFile[-1]["vectors"] and jsonFile[0][i]["color"] and len(jsonFile[0][i]["pos"]) == len(jsonFile[0][i]["values"]):
                        temp_objs.append(
                            create_plane(jsonFile[-1]["vectors"], jsonFile[0][i]["pos"], jsonFile[0][i]["values"], jsonFile[0][i]["color"])
                        )
                    else:
                        if useErrorCube: temp_objs.append((0, errorCube.vectors, errorCube.edges, True, True, errorCube.color))
                for i in jsonFile[1]:
                    temp_objs.append((1, i))
                for i in jsonFile[2]:
                    temp_objs.append((2, i))
                porsion = jsonFile[-1]["porsion"]
                objs = temp_objs
        except:
            if useErrorCube: objs = [(0, errorCube.vectors, errorCube.edges, True, True, errorCube.color)]

def stop():
    global run
    run = False


def get_info():
    global objs, cams, porsions
    return [objs, cams, porsion]


# Variables -------------------------------------------------------------------------------------------------------------------------- #

clock = pygame.time.Clock()
fps = 60; run = True; porsion = -1

# Cube
cubeVectors = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]])
cubeEdges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]

errorCube = Object([0, 0, 0], cubeVectors, cubeEdges, useEdges=True, color=(255, 0, 0))

# Dots
dots = [[0, 0, 0, (255, 255, 0)]]

objs = []; cams = []; graphs = ()


# start()