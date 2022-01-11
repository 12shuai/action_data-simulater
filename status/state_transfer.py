import numpy as np
from .state import StatusDict,Status
from collections import OrderedDict
from ..utils import ELExceptionString,ELExceptionRaise
class Stepper:
    MAXI_INTERVAL=1E-3
    MINI_INTERVAL=1E-8
    def __init__(self,func,interval):
        if not isinstance(func,StateTrasferFunc):
            raise TypeError("The input function should be StateTranferFunc type")
        if not self.MINI_INTERVAL<interval<self.MAXI_INTERVAL:
            raise Exception(f"The interval should in [{self.MINI_INTERVAL},{self.MAXI_INTERVAL}]")
        self.func=func
        self.interval=interval


    def __call__(self,status,input):
        update=self.func(status,input)*self.interval
        return status+update

class StateTrasferFunc:
    """需要重写 _mapStatusandInput(self,stateDict,input)，并定义stateName,InputName,（有序的字典对象，对应A,B转移矩阵）A，B转移矩阵"""
    def __init__(self,stateName=None,inputName=None,A=None,B=None):
        if not stateName or not inputName or not A or not B:
            raise Exception("Please complete definition of stateName, inputName, A and B")
        if isinstance(stateName,dict):
            stateName=OrderedDict(stateName)
        if isinstance(inputName,dict):
            inputName=OrderedDict(inputName)
        if not isinstance(stateName,OrderedDict) or not  isinstance(inputName,OrderedDict):
            raise TypeError("Both inputs should be dict(python) or OrderedDict type")
        self.stateName=stateName
        self.inputName=inputName
        self.A=A
        self.B=B

    def check(self,stateDict,input):
        """判断输入的状态字典的键是否正确，错误应该raise 错误原因"""
        try:
            ELExceptionRaise(self.stateName, stateDict, "State")
            ELExceptionRaise(self.inputName, input, "Input")
        except Exception as e:
            raise e


    def __call__(self, state,input):
        try:
            self.check(state,input)
        except Exception as e:
            raise e
        return self.forward(state,input)

    def forward(self,state,input):
        """根据当前状态和输入，输出更新值"""
        status,input=self._mapStatusandInput(state,input)
        resNp=self._forward(state,input)
        res=StatusDict()
        for index,k,_ in enumerate(self.stateName.items()):
            res.append(Status(k,resNp[index][0]))

        return res


    def printStateName(self):
        for index,k,v in enumerate(self.stateName.items()):
            print(f"The {index}th state:{k}")


    def printInputName(self):
        for index,k,v in enumerate(self.inputName.items()):
            print(f"The {index}th input:{k}")


    def _forward(self,state,input):
        update=self.A*state+self.B*input
        return update


    def _mapStatusandInput(self,stateDict,input):
        """根据当前状态和输入，输出更新值"""
        raise NotImplementedError()



class PVStateTransferFunc(StateTrasferFunc):
    def __init__(self):
        A=np.array([[0,0,0,1,0,0],
                     [0,0,0,0,1,0],
                     [0,0,0,0,0,1],
                     [0,0,0,0,0,0],
                     [0,0,0,0,0,0],
                     [0,0,0,0,0,0]])
        B=np.array([[0,0,0],
                     [0,0,0],
                     [0,0,0],
                     [1,0,0],
                     [0,1,0],
                     [0,0,1]])
        super(PVStateTransferFunc,self).__init__({"positionx":None,"positiony":None,"positionz":None,"velocityx":None,"velocity":None,"velocityz":None},
                                                 {"acceleratex":None,"acceleratey":None,"acceleratez":None},A,B)



    def _mapStatusandInput(self,stateDict,input):
        if isinstance(stateDict,StatusDict):
            stateDict=stateDict.dict
        if isinstance(input,StatusDict):
            input=input.dict

        if not isinstance(stateDict,dict) or not isinstance(input,dict):
            raise TypeError("Both inputs should be dict(python) or StatusDict type")
        try:
            ELExceptionRaise(self.stateName,stateDict,"State")
            ELExceptionRaise(self.inputName,input,"Input")
        except Exception as e:
            raise e

        state=np.ndarray([len(self.stateName),1])
        inp= np.ndarray([len(self.inputName),1])
        for index,k in enumerate(self.stateName):
            state[index]=stateDict[k]

        for index,k in enumerate(self.inputName):
            inp[index]=input[k]


        return state,inp





