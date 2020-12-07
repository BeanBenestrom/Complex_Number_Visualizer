import numpy, json, time
from threading import Thread
from random import randint
from functions import *
from math import *


# Classes ----------------------------------------------------------------------------------------------------------------------------- #

class Graph:
    def __init__(self, pos, variables, func=None, showRoots=False, color=None):
        self.pos = pos; self.roots = None; variables.reverse()
        self.variables = variables
        self.color = color
        self.func = func
        if not func: func = make_quadratic
        if showRoots and func == make_quadratic:
            i = pow(-(variables[1]/variables[2])/2, 2) - variables[0]/variables[2]
            if i < 0: i = sqrt(abs(i))
            else: i = sqrt(i) * 1j
            self.roots = [complex(-(variables[1]/variables[0])/2, i), complex(-(variables[1]/variables[0])/2, -i)]
            # print(a * self.roots[0] * self.roots[0] + b * self.roots[0] + c)
            # print(a * self.roots[1] * self.roots[1] + b * self.roots[1] + c)
        # print(variables.reverse())
        self.graph = make_graph(self, func)


# Graph functions --------------------------------------------------------------------------------------------------------------------- #

def make_graph(graph, func):
    positions = get_pos(graph)
    _graph = get_values(graph, positions, func)
    return [positions, _graph]


def get_pos(graph):
    positions = []
    for y in range(0, quality+1):
        y = y/quality*2*area-area+graph.pos[1]; # line = ""
        # print("y", y)
        for x in range(0, quality+1):
            x = 2*area/quality*x-area+graph.pos[0]
            # print("x", x)
            positions.append([x, y])
    return numpy.array(positions)


def get_values(graph, positions, func):
    _graph = []
    for i in positions:
        _graph.append(func(graph.variables, i[0], i[1]))
    return _graph


def get_color(positions):
    for i in positions:
        pass


# Graph equations ---------------------------------------------------------------------------------------------------------------------- #

def circle_movement():
    global usedLoopGraphs
    x = -2.5; z = 0; rot = 1/360*2*pi
    o = [0, 1]
    while True:
        time.sleep(0.01)
        x = x*cos(rot) - z*sin(rot)
        z = x*sin(rot) + z*cos(rot)
        for i in usedLoopGraphs:
            i.pos[0] = o[0] + x
            i.graph = make_graph(i, i.func)
        save_json()


def AI_derivative_movement(_graph, x, z, speed=1):
    global usedLoopGraphs, dots
    with open("AI.json") as f:
        f = json.load(f)
        print(x, z)
        # print(linear_regression_func(_graph.variables, x, z)[0])

        for i in range(0, len(f[0])):
            dots.append([(f[0][i], f[1][i] ,0), (255, 200, 0), 5])

        dot = [(x, linear_regression_func(_graph.variables, x, z)[0], z), (255, 0, 0), 5]
        dotPos = len(dots); dots.append(dot)

        lineAI = [(0, 0, 0), (10, 0, 0), (255, 155, 0), 3]
        lines.append(lineAI)
        # lx = [(0, 0, 0), (x, 0, 0), (255, 0, 0), 1]
        # lz = [(x, 0, 0), (x, 0, z), (0, 0, 255), 1]
        # ly = [(x, 0, z), (x, linear_regression_func(_graph.variables, x, z)[0], z), (0, 255, 0), 1]
        # lines.append(lx); lines.append(lz); lines.append(ly)

        # xDer = [(dot[0], dot[1], dot[2]), (dot[0], dot[1], dot[2]), (255, 0, 0), 5]
        xDer = [(0, 0, 0), (0, 0, 0), (255, 0, 0), 2]
        zDer = [(0, 0, 0), (0, 0, 0), (0, 0, 255), 2]
        lines.append(xDer); lines.append(zDer)

        xi = f[0]; yi = f[1]

        while True:
            time.sleep(0.01)
            _x = 0; _z = 0
            for i in range(0, len(xi)):
                _x += (2*x*pow(xi[i], 2)+2*z*xi[i]-2*xi[i]*yi[i])*(1/len(xi))
            for i in range(0, len(xi)):
                _z += (2*x*xi[i]+2*z-2*yi[i])*(1/len(xi))
            print(_x, _z)
            x -= _x*speed; z -= _z*speed
            print(x, z)
            print()
            dot[0] = (x, linear_regression_func(_graph.variables, x, z)[0], z)
            xDer[0] = (dot[0][0]-0.1, dot[0][1]-_x*0.1, dot[0][2]); xDer[1] = (dot[0][0]+0.1, dot[0][1]+_x*0.1, dot[0][2])
            zDer[0] = (dot[0][0], dot[0][1]-_z*0.1, dot[0][2]-0.1); zDer[1] = (dot[0][0], dot[0][1]+_z*0.1, dot[0][2]+0.1)
            lineAI[0] = [0, dot[0][2], 0]; lineAI[1] = [10, dot[0][0]*10+dot[0][2], 0]
            save_json()


# JSON -------------------------------------------------------------------------------------------------------------------------------- #

def save_json():
    # test = [
    #     [[[0], [0]], [[0], [0]]],
    #     [[[1], [1]], [[3], [3]]],
    #     [[[4], [4]], [[5], [5]]]
    # ]

    json_text = [[], [], []]
    for i in graphs:
    #                  {"pos" : [[1, 2], [5, 2]], "values" : [[2, 2], [1, 2]]}
        # print(i.graph[1])

        value = []
        for num in i.graph[1]:
            # print(type(num) == complex)
            if type(num) == complex:
                value.append((round(num.real, roundAmount), round(num.imag, roundAmount)))
            else:
                value.append((round(num[0], roundAmount), round(num[1], roundAmount)))

        json_text[0].append(
            {
                "pos" : [(round(x, roundAmount), round(y, roundAmount)) for x, y in i.graph[0].tolist()],
                "values" : value,
                "color" : i.color
            }
        )

    for i in lines:
        json_text[1].append(i)

    for i in dots:
        json_text[2].append(i)

    json_text.append({"size" : size, "vectors" : quality, "porsion" : porsion, "errorCube" : useErrorCube})

    with open("graph_info.json", "w") as f:
        json.dump(json_text, f)


# Variables ---------------------------------------------------------------------------------------------------------------------------- #

area = 1
size = 1
quality = 50
porsion = 100
roundAmount = 3   # To what decimal the numbers will be rounded for the JSON file
useErrorCube = True

# Graph -------------------------------------------------------------------------------------------------------------------------------- #

#g1 = Graph([0, 0], [3, 6, 5], func=make_quadratic, color=(255, 100, 100))
#g2 = Graph([0, 0], [1, 0, 1], func=make_quadratic, showRoots=True, color=(100, 255, 100))
#g3 = Graph([0, 0], [1, 1, 1], func=make_quadratic, color=(100, 100, 255))
#g4 = Graph([-0.2, 0], [1, 1, 1, 1, 1, 1], func=make_q5, color=(255, 100, 100))
#g5 = Graph([0, 0], [0, 0], func=plane_test, color=(255, 255, 255))
#g6 = Graph([-0.4, 0], [0.001, 0.01, 1, 1, 1, 1, 0], func=make_q6, color=(100, 100, 255))
#gSin = Graph([0, 0], [], func=sin_func, color=(200, 200, 255))
#gCos = Graph([0, 0], [], func=cos_func, color=(200, 255, 200))
# print(g1.graph)
# print(g1.roots)
# graphs = [g1, g2]

plane  = Graph([-2.5, 9.5], [0, 0], func=plane_test, color=(255, 255, 255))
line1 = [(0, 0, 0), (5, 5, 0), (255, 0, 0), 5]
line2 = [(5, 0, 5), (5, 5, 5), (255, 255, 0), 1]
dot1 = [(5, 5, 5), (255, 0, 0), 5]

with open("AI.json") as f:
    f = json.load(f)
    print(f[2])
    lineAIZ = [(0, 0, 0), (0, 0, f[2][1]), (0, 0, 255), 5]
    lineAIX = [(0, 0, f[2][1]), (f[2][0], 0, f[2][1]), (255, 0, 0), 5]
    # lg = Graph([2, 0], [[1, 2, 3, 4, 5], [2, 4, 6, 8, 10], 5], func=linear_regression_func, color=(50, 150, 200))
    lg = Graph([f[2][0], f[2][1]], [f[0], f[1], len(f[0])], func=linear_regression_func, color=(50, 150, 200))

graphs = [lg]
usedLoopGraphs = []

lines = [line1, line2, lineAIZ, lineAIX]
dots = [dot1]


save_json()
AI_derivative_movement(lg, randint(-area*1000, area*1000)/100, randint(-area*1000, area*1000)/100, 0.1)
