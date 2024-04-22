# import numpy module for matrix computing
import numpy as np


# define AND function
def AND(x1, x2):
    x = np.array([1, x1, x2])
    w = np.array([-0.7, 0.5, 0.5])
    tmp = np.dot(x,w)
    # tmp = np.sum(w * x)
    if tmp <= 0:
        return 0
    else:
        return 1


# define AND function
def OR(x1, x2):
    x = np.array([1, x1, x2])
    w = np.array([-0.2, 0.5, 0.5])
    tmp = np.sum(w * x)
    if tmp <= 0:
        return 0
    else:
        return 1


# define AND function
def NAND(x1, x2):
    y = AND(x1,x2)
    return 0 if y == 1 else 1


# define AND function
def XOR(x1, x2):
    #     y
    #     |
    # --------- layer 2
    # |   |   |
    # 1  y1  y2
    # |   |   |
    # --------- layer 1
    # |   |   |
    # 1   x2  x2

    y1 = OR(x1,x2)
    y2 = NAND(x1,x2)
    print([x1, x2])
    return AND(y1,y2)



    y = [1,y1,y2]

    # print(y)
    w = np.array([-0.7, 0.5, 0.5])
    tmp = np.sum(w * y)
    if tmp <= 0:
        return 0
    else:
        return 1


print(XOR(0,0))
print(XOR(0,1))
print(XOR(1,0))
print(XOR(.9,.9))

print(AND(.0, 1))
print(AND(.8, .9))
print(OR(.0, .9))
