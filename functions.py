from math import *

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


def sin_func(_, x, y):
    return complex(sin(x), y)


def cos_func(_, x, y):
    return complex(cos(x), y)


def linear_regression_func(var, x, y):
    value = 0
    # print(var[2], var[1])
    for i in range(0, var[0]):
        value += pow((x*var[2][i]+y)-var[1][i], 2)*(1/var[0])
    return [value, y]
