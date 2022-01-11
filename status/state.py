from ..utils import ELExceptionString
from collections import  OrderedDict
import numpy as np
import math

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
    def __init__(self,*status):
        self.dict=OrderedDict()
        for sta in status:
            self.dict[sta.name]=sta.value

    def append(self,status):
        self.dict[status.name]=status.value

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key]=value


    def __len__(self):
        return len(self.dict)


    def items(self):
        return self.dict.items()

    def keys(self):
        return self.dict.keys()


    def __add__(self, other):
        if not isinstance(other,StatusDict):
            raise TypeError("Variable should be both StatusDict type..")
        if set(self.dict)!=set(other.dict):
            raise TypeError("Variable's namespace should be the same.. ")
        res=StatusDict()
        for k,v in self.dict:
            res.append(v+other[k])

        return res

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

    def toNp(self):
        return np.array(self.toList())

    def fromNp(self,n):
        list=n.tolist()
        self.fromList(list)

    def norm(self):
        value = 0
        for k, v in self.items():
            value += v ** 2

        return math.sqrt(value)






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
        if isinstance(statusDict,StatusDict):
            statusDict=statusDict.dict

        if not isinstance(statusDict,dict):
            raise TypeError("Input should be dict(python) or StateDict type")

        if set(dict)!=self.stateName:
            raise Exception(ELExceptionString(self.stateName,dict))

        for k,v in dict.items():
            self.tracer[k].append(v)
            self.lenth+=1


    def __iter__(self):
        return self

    def __next__(self):
        if self.curr==self.lenth:
            raise StopIteration()
        res=StatusDict()
        for k,v in self.tracer:
            res.append(Status(k,v))
        self.curr+=1
        return res
