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


def x2_y2(_, x, y):
    return [pow(x, 2) + pow(y, 2), y]


def x_y_times_2(_, x, y):
    return [x*2 + y*2, y]


def inverse_kinematic_regression_func(var, x, y):
    value = pow(var[0]*cos(x)+var[0]*cos(y)-var[2], 2) + pow(var[0]*sin(x)+var[0]*sin(y)-var[1], 2)
    # value = sqrt(pow(var[0]*cos(x)+var[0]*cos(y)-var[2], 2) + pow(var[0]*sin(x)+var[0]*sin(y)-var[1], 2))
    return [value, y]


def inverse_kinematic_regression_dev(var, x, y):
    X, Y, C = var[2], var[1], var[0]
    # print(var0, var1, var2, var3)
    z = y
    return [2*(C*cos(x)+C*cos(y)-X)*(C*(-sin(x)))+2*(C*sin(x)+C*sin(y)-Y)*(C*cos(x)), 
            2*(C*cos(x)+C*cos(y)-X)*(C*(-sin(y)))+2*(C*sin(x)+C*sin(y)-Y)*(C*cos(y))]
    # return [2*(C*cos(x)+C*cos(y)-X)*(C*(-sin(x)))+2*(C*sin(x)+C*sin(y)-Y)*(C*cos(x))/
    #         sqrt(pow(C*cos(x)+C*cos(y)-X, 2)), 
    #         2*(C*cos(x)+C*cos(y)-X)*(C*(-sin(y)))+2*(C*sin(x)+C*sin(y)-Y)*(C*cos(y))/
    #         sqrt(pow(C*cos(x)+C*cos(y)-X, 2))]

def inverse_kinematic_regression_dev_XY(var, x, y):
    var0, X, Y, C = var[0], var[3], var[2], var[1]
    z = y
    if var0 == 0:
        # 0dev: 2*(C*cos(01)+C*cos(02)-X)*(C*(-sin(01))) + 2*(C*sin(01)+C*sin(02)-Y)*(C*cos(01))
        # 1dev: 2*(C*cos(01)+C*cos(02)-X)*(C*(-sin(02))) + 2*(C*sin(01)+C*sin(02)-Y)*(C*cos(02))        
        return [2*(C*cos(x)+C*cos(y)-X)*(C*(-sin(x)))+2*(C*sin(x)+C*sin(y)-Y)*(C*cos(x))/
                sqrt(pow(C*cos(x)+C*cos(y)-X, 2)+pow(C*sin(x)+C*sin(y)-Y, 2)), z]

    return [2*(C*cos(x)+C*cos(y)-X)*(C*(-sin(y)))+2*(C*sin(x)+C*sin(y)-Y)*(C*cos(y))/
            sqrt(pow(C*cos(x)+C*cos(y)-X, 2)+pow(C*sin(x)+C*sin(y)-Y, 2)), z]


    #     return [1/(2*sqrt(pow(var3*cos(x)+var3*cos(z)-var1, 2) + pow(var3*sin(x)+var3*sin(z)-var2, 2))
    #     )*(pow(var3, 2)*2*cos(x)*(-sin(x))+2*pow(var3, 2)*cos(z)*(-sin(x))+2*var1*var3*(-sin(x))+
    #     pow(var3, 2)*2*sin(x)*(cos(x))+2*pow(var3, 2)*sin(z)*(cos(x))+2*var2*var3*(cos(x))), z]
    # return [1/(2*sqrt(pow(var3*cos(z)+var3*cos(x)-var1, 2) + pow(var3*sin(z)+var3*sin(x)-var2, 2))
    # )*(pow(var3, 2)*2*cos(z)*(-sin(z))+2*pow(var3, 2)*cos(x)*(-sin(z))+2*var1*var3*(-sin(z))+
    # pow(var3, 2)*2*sin(z)*(cos(z))+2*pow(var3, 2)*sin(x)*(cos(z))+2*var2*var3*(cos(z))), z]




# def other_inverse_kinematic_regression_func(var, x, y):
#     return [sqrt(pow(var[0]*cos(x)+var[0]*cos(x)-var[2], 2) + pow(var[0]*sin(y)+var[0]*sin(y)-var[1], 2)), y]
