from status import StatusDict,ELExceptionRaise,dict2statedict
from itertools import chain
from utils import *

class InputComposer:
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
    def __init__(self,nameSet,initState=None,lenth=None,tracer=None):
        if not lenth:
            self.mode=self.INFINITE
        else:
            self.mode=self.FINITE
            self.lenth=lenth
        self.nameSet=nameSet
        self.tracer=tracer
        self.initState=None
        if initState:

            try:
                self.checkState(initState)
                self.initState = dict2statedict(initState)

            except Exception as e:
                raise e



    def setTracer(self,tracer):
        self.tracer=tracer

    def __iter__(self):
        return self

    def produce(self):
        res=self._produce()

        try:
            self.checkState(res)
        except Exception as e:
            raise e
        return dict2statedict(res)


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

        ELExceptionRaise(self.nameSet,state,"State")









##0.加速模型
class AccelerateMaker(InputMaker):
    def __init__(self,initState,lenth=None,tracer=None):
        super(AccelerateMaker,self).__init__({"acceleratex","acceleratey","acceleratez"},initState,lenth,tracer)
    def _produce(self):
        raise NotImplementedError()



##1.无/常加速度模型
class ConstantAccelerateMaker(AccelerateMaker):
    def __init__(self,initState=None,lenth=None,tracer=None):
        if not initState:
            initState={"acceleratex":0,"acceleratey":0,"acceleratez":0}
        super(ConstantAccelerateMaker,self).__init__(initState,lenth,tracer)
    def _produce(self):
        return self.initState

##2.变加速度模型
class VarAccelerateMaker(AccelerateMaker):

    def __init__(self,scheduler,initState=None,lenth=None,tracer=None):
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
        super(VarAccelerateMaker,self).__init__(initState,lenth,tracer)


    def _produce(self):
        return self.scheduler()



##2.1圆心常加速度运动模型
class NormalAccelerateMaker(VarAccelerateMaker):

    def __init__(self,initState,lenth=None,tracer=None):


        super(NormalAccelerateMaker,self).__init__(self.f,initState,lenth,tracer)


    def _produce(self):

        res=super(NormalAccelerateMaker, self)._produce()
        return res

    def f(self,state):
        axis = normalize(rotate90cc(self.tracer.getStateDict(-1,["velocityx","velocityy","velocityz"]).toNP()))
        newState = state.norm() * axis
        return dict2statedict({"acceleratex": newState[0], "acceleratey": newState[1], "acceleratez": newState[2]})


##2.2固定半径的圆周运动
class CircleAccelerateMaker(NormalAccelerateMaker):

    def __init__(self,raidus,lenth=None,tracer=None):
        self.radius=raidus
        initStateList=self.tracer.getStateDict(-1,["acceleratex","acceleratey","acceleratez"]).norm()**2/raidus
        initState=dict2statedict({"acceleratex": initStateList[0], "acceleratey": initStateList[1], "acceleratez": initStateList[2]})

        super(CircleAccelerateMaker,self).__init__(initState,lenth,tracer)




#3.左转弯模型
class VarAccelerateMaker(AccelerateMaker):

    def __init__(self,scheduler,initState=None,lenth=None,tracer=None):
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
        super(VarAccelerateMaker,self).__init__(initState,lenth,tracer)


    def _produce(self):
        return self.scheduler()




