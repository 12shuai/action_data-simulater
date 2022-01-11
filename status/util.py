import math
from .state import StatusDict,Status
def statedict2dict(dic):
    if isinstance(dic,StatusDict):
        res={}
        for k,v in dic.dict:
            res[k]=v
        return res
    elif isinstance(dic,dict):
        return dic
    else:
        raise TypeError("Type should be dict(python) or StatusDict")


def dict2statedict(dic):
    if isinstance(dic,dict):
        res=StatusDict()
        for k,v in dic:
            res.append(Status(k,v))
        return res
    elif isinstance(dic,StatusDict):
        return dic
    else:
        raise TypeError("Type should be dict(python) or StatusDict")


def getNorm(state):
    value=0
    for k,v in state.items():
        value+=v**2

    return math.sqrt(value)

