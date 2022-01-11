from .status import Tracer,Stepper,statedict2dict,dict2statedict
from .utils import ELExceptionRaise
class Simulator:

    def __init__(self,initStatus,stepperFunc,interval,inputMaker,handler=None):
        self._init(initStatus,stepperFunc,interval,inputMaker)

        if isinstance(handler,list):
            self.handlers=handler
        else:
            self.handlers=[]
            self.handlers.append(handler)

    def _init(self,initStatus,stepperFunc,interval,inputMaker):
        self.initStatus = initStatus
        self.stepper = Stepper(stepperFunc, interval)
        try:
            ELExceptionRaise(stepperFunc.stateName,initStatus,"InitState")
        except Exception as e:
            raise e
        self.recorder = Tracer(set(statedict2dict(initStatus)))
        self.recorder.append(dict2statedict(initStatus))
        try:
            ELExceptionRaise(stepperFunc.inputName,inputMaker.nameSet,"Input")
        except Exception as e:
            raise e
        self.inputMaker = inputMaker



    def forward(self):
        state=self.initStatus
        for input in self.inputMaker:
            state=self.stepper(state,input)
            self.recorder.append(state)

        self.handle()


    def handle(self):
        for handler in self.handlers:
            handler.handle(self.recorder)



