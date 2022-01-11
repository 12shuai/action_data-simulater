import numpy as np
import numpy.linalg as linalg
CLOCK=0
COUNTER_CLOCK=1
"""可以返回工厂"""

def rotateByAxis(vector,Axis,degree,orient=COUNTER_CLOCK):
    """vector逆时时针旋转degree(单位为度)"""
    if orient==COUNTER_CLOCK:
        alpha =-(degree/180) * np.pi
    elif orient==CLOCK:
        alpha=(degree/180) * np.pi
    else:
        raise Exception("orient only in [CLOCK(0),COUNTER_CLOCK(1)]")

    pass
def rotate90cc(vector,axis):
    return rotateByAxis(vector,axis,90)

def rotate90c(vector,axis):
    return rotateByAxis(vector,axis,90,orient=CLOCK)



def rotateByMatrix(vector,matrix):
    return matrix*vector




def rotateByEuler(vector,*eulerAngle):
    pass

def rotateByQuater(vector,*quater):
    pass


def normalize(vector):
    return linalg.norm(vector)