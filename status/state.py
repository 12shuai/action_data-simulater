from collections import  OrderedDict
import numpy as np
import math
from copy import deepcopy
import random



class Status:
    def __init__(self,name,value):
        self.name=name
        self.value=value

    def __add__(self, other):
        if not isinstance(other,Status):
            raise TypeError("Variable should be both Status type..")

        if self.name!=other.name:
            raise Exception("Varaible's name should be the same")

        return Status(self.name,self.value+other.value)



class StatusDict(OrderedDict):
    def __init__(self,stateDict={}):
        self.dict=OrderedDict(statedict2dict(stateDict))

    def __iter__(self):
        return self.dict

    def append(self,status):
        self.dict[status.name]=status.value

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key]=value


    def __len__(self):
        return len(self.dict)

    def __str__(self):
        return self.dict.__str__()
    def __repr__(self):
        return self.dict.__repr__()


    def __mul__(self, other):
        res=self.copy()
        for k,v in res.items():
            res[k]=other*v

        return res

    def update(self,stateDict):
        self.dict.update(statedict2dict(stateDict))


    def items(self):
        return self.dict.items()

    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()


    def __add__(self, other):
        if not isinstance(other,StatusDict):
            raise TypeError("Variable should be both StatusDict type..")
        if set(self.dict)!=set(other.dict):
            raise TypeError("Variable's namespace should be the same.. ")
        res=self.copy()
        for k,v in res.items():
            res[k]=v+other[k]

        return res

    def getSubStatus(self,names):
        if not isinstance(names,list):
            raise  TypeError("names should be list type")
        res={}
        try:
            for k in names:
                res[k]=self[k]
        except Exception as e:
            raise e
        return StatusDict(res)


    def copy(self):
        return StatusDict(deepcopy(self.dict))


    def toList(self):
        res=[]
        for _,v in self.items():
            res.append(v)

        return res

    def fromList(self,list):
        if len(list)!=len(self):
            raise Exception("Input dim don't match the dict dim")
        for index,k in enumerate(self.keys()):
            self[k]=list[index]
        return self

    def toNp(self):
        return np.array(self.toList())

    def fromNp(self,n):
        list=n.tolist()
        return self.fromList(list)



    def toDict(self):
        return self.dict

    def fromDict(self,dict):
        self.update(dict)
        return self

    def norm(self):
        value = 0
        for k, v in self.items():
            value += v ** 2

        return math.sqrt(value)


    def randomKey(self,*keys,min=None,max=None):
        if not keys:
            keys=self.keys()
        for key in keys:
            if isinstance(key, list):
                self.randomKey(*key)
            else:
                if min is None and max is None:
                    for k in self.keys():
                        self[k] = random.random()
                    return self
                elif min is not None and max is not None:
                    if max <= min:
                        raise Exception("max must be larger than min")
                    for k in self.keys():
                        self[k] = random.random()*(max-min)+min
                    return self

                else:

                    raise Exception("min or max should be both None or not None")



def findEL(src, dst):
    """返回[缺少的键，多余的键】"""
    sKey = set(src)
    dKey = set(dst)
    return [sKey - dKey, dKey - sKey]


def ELExceptionString(src,dst,name="Input"):
    loss,extra=findEL(src,dst)
    return f"{name}'s key space do not satisfy, loss:{loss}, extra:{extra}"


def ELExceptionRaise(src,dst,name="Input"):

    if isinstance(src,StatusDict):
        src=statedict2dict(src)
    if isinstance(dst,StatusDict):
        dst=statedict2dict(dst)

    if set(src) != set(dst):
        raise Exception(ELExceptionString(src,dst,name))


def statedict2dict(dic):
    if isinstance(dic,StatusDict):

        return dic.toDict()
    elif isinstance(dic,dict):
        return dic
    else:
        raise TypeError("Type should be dict(python) or StatusDict")


def dict2statedict(dic):
    if isinstance(dic,dict):

        res=StatusDict()

        return res.fromDict(dic)
    elif isinstance(dic,StatusDict):

        return dic
    else:
        raise TypeError("Type should be dict(python) or StatusDict")


def getNorm(state):
    value=0
    for k,v in state.items():
        value+=v**2

    return math.sqrt(value)



def generatePV():
    return StatusDict({"positionx":0,"positiony":0,"positionz":0,"velocityx":0,"velocity":0,"velocityz":0})



def generateRandomPV():
    return StatusDict({"positionx":0,"positiony":0,"positionz":0,"velocityx":0,"velocity":0,"velocityz":0}).randomKey()







def _makeTracer(stateName):
    res={}
    for k in stateName:
        res[k]=[]
    return res

class Tracer:
    def __init__(self,stateName):
        self.stateName=stateName
        self.tracer=_makeTracer(stateName)
        self.curr=0
        self.lenth=0

    def append(self,statusDict):
        ELExceptionRaise(self.stateName,statusDict)

        for k,v in statusDict.items():
            self.tracer[k].append(v)
        self.lenth+=1


    def getStateDict(self,index,names=None):
        res={}
        if not names:
            for k,v in self.tracer.items():
                res[k]=self.tracer[k][index]
        else:
            if not isinstance(names,list):
                raise TypeError("names should be list type")

            for k in names:
                res[k]=self.tracer[k][index]

        return StatusDict(res)


    def __iter__(self):
        return self

    def __next__(self):
        if self.curr==self.lenth-1:
            self.curr=0
            raise StopIteration()
        res=StatusDict()
        for k,v in self.tracer.items():

            res.append(Status(k,v[self.curr]))
        self.curr+=1
        return res
