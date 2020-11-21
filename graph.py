import numpy, json
from math import *


# Classes ----------------------------------------------------------------------------------------------------------------------------- #

class Graph:
    def __init__(self, pos, variables, func=None, showRoots=False, color=None):
        self.pos = pos; self.roots = None; variables.reverse()
        self.variables = variables
        self.color = color
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

def make_q6(var, x, y):
    # print(var)
    return  complex(var[6]) * complex(x, y)**6 + complex(var[5]) * complex(x, y)**5 + complex(var[4]) * complex(x, y)**4 + complex(var[3]) * complex(x, y)**3 + complex(var[2]) * complex(x, y)**2 + complex(var[1]) * complex(x, y) + complex(var[0])


def make_q5(var, x, y):
    # print(var)
    return  complex(var[5]) * complex(x, y)**5 + complex(var[4]) * complex(x, y)**4 + complex(var[3]) * complex(x, y)**3 + complex(var[2]) * complex(x, y)**2 + complex(var[1]) * complex(x, y) + complex(var[0])


def make_q4(var, x, y):
    # print(var)
    return  complex(var[4]) * complex(x, y)**4 + complex(var[3]) * complex(x, y)**3 + complex(var[2]) * complex(x, y)**2 + complex(var[1]) * complex(x, y) + complex(var[0])


def make_qubic(var, x, y):
    # print(var)
    return  complex(var[3]) * complex(x, y)**3 + complex(var[2]) * complex(x, y)**2 + complex(var[1]) * complex(x, y) + complex(var[0])


def make_quadratic(var, x, y):
    # print(var)
    return  complex(var[2]) * complex(x, y)**2 + complex(var[1]) * complex(x, y) + complex(var[0])


def make_q1(var, x, y):
    # print(var)
    return complex(var[1]) * complex(x, y) + complex(var[0])


def plane_test(_, x, y):
    return complex(0, y)


# Variables ---------------------------------------------------------------------------------------------------------------------------- #

area = 1.5
size = 1
quality = 30
porsion = 10
roundAmount = 2    # To what decimal the numbers will be rounded for the JSON file

# Graph -------------------------------------------------------------------------------------------------------------------------------- #

g1 = Graph([0, 0], [3, 6, 5], func=make_quadratic, color=(255, 100, 100))
g2 = Graph([0, 0], [1, 1, 1], func=make_quadratic, showRoots=True, color=(100, 255, 100))
g3 = Graph([0, 0], [1, 1, 1], func=make_quadratic, color=(100, 100, 255))
g4 = Graph([0, 0], [0.01, 0.01, 1, 1, 1, 0], func=make_q5, color=(255, 100, 100))
g5 = Graph([0, 0], [0, 0], func=plane_test, color=(255, 255, 255))
g6 = Graph([-0.4, 0], [0.001, 0.01, 1, 1, 1, 1, 0], func=make_q6, color=(100, 100, 255))
# print(g1.graph)
# print(g1.roots)
# graphs = [g1, g2]
graphs = [g4]


# JSON -------------------------------------------------------------------------------------------------------------------------------- #

# test = [
#     [[[0], [0]], [[0], [0]]], 
#     [[[1], [1]], [[3], [3]]], 
#     [[[4], [4]], [[5], [5]]]
# ]

json_text = []
for i in graphs:
#                  {"pos" : [[1, 2], [5, 2]], "values" : [[2, 2], [1, 2]]}
    # print(i.graph[1])
    json_text.append(
        {
            "pos" : [(round(x, roundAmount), round(y, roundAmount)) for x, y in i.graph[0].tolist()], 
            "values" : [(round(num.real, roundAmount), round(num.imag, roundAmount)) for num in i.graph[1]],
            "color" : i.color
        }
    )
json_text.append({"size" : size, "vectors" : quality, "porsion" : porsion})

with open("graph_info.json", "w") as f:
    json.dump(json_text, f)
