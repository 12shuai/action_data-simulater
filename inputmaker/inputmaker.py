from ..status import StatusDict,statedict2dict,dict2statedict,getNorm
from itertools import chain
from ..utils import *

class Composer:
    def __init__(self,*inputMaker):
        self.nameSet = None
        try:
            self.check(inputMaker)
        except Exception as e:
            raise e
        self.inputMaker=inputMaker


    def check(self,*inputMaker):
        if not inputMaker:
            raise Exception("Composer should have at least one InputMaker")

        for inp in inputMaker:
            if not isinstance(inp,InputMaker):
                raise TypeError("The input should be InputMaker type")
            if not self.nameSet:
                self.nameSet=inp.nameSet
                continue
            if self.nameSet!=inp.nameSet:
                raise Exception("The inputs(InputMaker type) should have same nameSet")

        return

    def __iter__(self):
        return chain.from_iterable(self.inputMaker)



class InputMaker:
    INFINITE=0
    FINITE=1
    def __init__(self,nameSet,lenth=None):
        if not lenth:
            self.mode=self.INFINITE
        else:
            self.mode=self.FINITE
            self.lenth=lenth
        self.nameSet=nameSet

    def __iter__(self):
        return self

    def produce(self):
        res=self._produce()
        try:
            self.checkState(res)
        except Exception as e:
            raise e
        return res


    def _produce(self):
        raise NotImplementedError()

    def __next__(self):
        if self.mode:
            while self.lenth:
                self.lenth-=1
                return self.produce()
            raise StopIteration()

        else:
            try:
                while True:
                    return self.produce()
            except InterruptedError:
                raise StopIteration()
            except Exception as e:
                raise e

    def checkState(self,state):
        if not isinstance(state,StatusDict):
            raise TypeError("Wrong type (StatusDict type needed)")
        if set(state.dict)!=set(self.nameSet):
            raise Exception("Wrong states, "+ELExceptionString(self.nameSet,state.dict,"State"))









##0.加速模型
class AccelerateMaker(InputMaker):
    def __init__(self,initState,lenth=None):
        super(AccelerateMaker,self).__init__({"acceleratex","acceleratey","acceleratez"},lenth)
        try:
            self.checkState(initState)
        except Exception as e:
            raise e
        self.initState =initState




##1.无/常加速度模型
class ConstantAccelerateMaker(AccelerateMaker):
    def __init__(self,initState=None,lenth=None):
        if not initState:
            initState=dict2statedict({"acceleratex":0,"acceleratey":0,"acceleratez":0})
        super(ConstantAccelerateMaker,self).__init__(initState,lenth)
    def _produce(self):
        return self.initState

##2.变加速度模型
class VarAccelerateMaker(AccelerateMaker):

    def __init__(self,scheduler,initState=None,lenth=None):
        """scheduler接受StateDict，或者dict为输入，并输出下一时刻的加速度"""
        if not initState:
            initState=dict2statedict({"acceleratex":0,"acceleratey":0,"acceleratez":0})

        def decorate(f,state):

            def ff():
                nonlocal state
                newState=f(state)
                yield state
                state=newState

            return ff

        self.scheduler=decorate(scheduler,initState)
        super(VarAccelerateMaker,self).__init__(initState,lenth)




    def _produce(self):
        return self.scheduler()



##2.1圆心常加速度运动模型
class NormalAccelerateMaker(VarAccelerateMaker):

    def __init__(self,initVelocity,initState,interval,lenth=None):
        def f(state):
            axis=normalize(rotate90cc(self.currentVelocity.toNP()))
            newState=state.norm()*axis
            return dict2statedict({"acceleratex":newState[0],"acceleratey":newState[1],"acceleratez":newState[2]})


        self.currentVelocity=initVelocity
        self.inertval=interval
        super(NormalAccelerateMaker,self).__init__(f,initState,lenth)


    def _produce(self):

        res=super(NormalAccelerateMaker, self)._produce()
        self.currentVelocity+=self.interval*res
        return res


##2.2固定半径的圆周运动
class CircleAccelerateMaker(NormalAccelerateMaker):

    def __init__(self,initVelocity,raidus,interval,lenth=None):
        self.radius=raidus
        initStateList=self.currentVelocity.norm()**2/raidus
        initState=dict2statedict({"acceleratex": initStateList[0], "acceleratey": initStateList[1], "acceleratez": initStateList[2]})

        super(CircleAccelerateMaker,self).__init__(initVelocity,initState,interval,lenth)








