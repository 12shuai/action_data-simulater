from status import Tracer,Stepper,statedict2dict,dict2statedict,ELExceptionRaise
class Simulater:

    def __init__(self,initStatus,stepperFunc,interval,inputMaker,handler=None):
        self._init(initStatus,stepperFunc,interval,inputMaker)

        if isinstance(handler,list):
            self.handlers=handler
        else:
            self.handlers=[]
            self.handlers.append(handler)

    def _init(self,initStatus,stepperFunc,interval,inputMaker):
        self.initStatus = initStatus.copy()

        self.stepper = Stepper(stepperFunc, interval)
        ELExceptionRaise(stepperFunc.stateName,self.initStatus,"InitState")
        self.recorder = Tracer(self.initStatus.keys())
        self.recorder.append(self.initStatus)
        ELExceptionRaise(stepperFunc.inputName,inputMaker.nameSet,"Input")

        self.inputMaker = inputMaker
        self.inputMaker.setTracer(self.recorder)



    def forward(self):
        state=self.initStatus
        for input in self.inputMaker:

            state=self.stepper(state,input)

            self.recorder.append(state)

        self.handle()




    def handle(self):

        for handler in self.handlers:
            handler.handle(self.recorder)



    def __call__(self, *args, **kwargs):
        self.forward()



