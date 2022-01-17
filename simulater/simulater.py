from status import Condition,Tracer,Stepper,ELExceptionRaise



class Simulater:

    def __init__(self,initStatus,condition,stepperFunc,interval,inputMaker,handler=None):
        self._init(initStatus,condition,stepperFunc,interval,inputMaker)
        if isinstance(handler,list):
            self.handlers=handler
        else:
            self.handlers=[]
            self.handlers.append(handler)

    def reset(self):
        self.recorder.reset()


    def setInitState(self,initStatus):
        self.initStatus=initStatus


    def setInterval(self,interval):
        self.stepper.setInterval(interval)



    def addHandler(self,*handler):
        self.handlers.extend(handler)


    def setHandler(self,handler):
        self.handlers=[handler] if not isinstance(handler,list) else handler


    def _init(self,initStatus,condition,stepperFunc,interval,inputMaker):
        self.initStatus = initStatus.copy()
        self.condition=Condition(condition)
        ELExceptionRaise(self.condition.stateName, self.initStatus, "Condition")
        self.stepper = Stepper(stepperFunc, interval)
        ELExceptionRaise(stepperFunc.stateName,self.initStatus,"StepperFunc")
        self.recorder = Tracer(self.initStatus.keys())
        self.recorder.append(self.initStatus)
        ELExceptionRaise(stepperFunc.inputName,inputMaker.nameSet,"InputMaker")

        self.inputMaker = inputMaker
        self.inputMaker.setTracer(self.recorder)



    def forward(self):
        state=self.initStatus
        for input in self.inputMaker:
            state=self.stepper(state,input)
            # print(self._correct(state))
            self.recorder.append(self._correct(state))

        self.handle()


    def _correct(self,state):

        return self.condition.correct(state)

    def handle(self):
        for handler in self.handlers:
            handler.handle(self.recorder)



    def __call__(self, *args, **kwargs):
        self.forward()



