from simulater import Simulater
from .environment import Environment

class Scheduler:
    """继承randomInitState"""
    def __init__(self,condition,setting,lenth,stepperFunc,interval):
        self.stepperFunc=stepperFunc
        self.condition=condition
        self.environment=Environment(condition,setting,lenth)
        self.interval=interval


    def forward(self):
        for initState,inputMaker,handler in self.environment:
            ##这样不高效！！

            simulater=Simulater(initState,self.condition,self.stepperFunc,self.interval,inputMaker,handler)
            simulater.forward()





