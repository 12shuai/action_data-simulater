import csv

from status import Tracer
import matplotlib.pyplot as plt


class Handler:

    def __init__(self):
        pass

    def handle(self,recoder):
        if not isinstance(recoder,Tracer):
            raise TypeError("Input should be Tracer type")
        self._handle(recoder)

    def _handle(self,recorder):
        raise NotImplementedError()




class CSVHandler(Handler):
    def __init__(self,path):
        self.path=path
        self.header=None
        super(CSVHandler, self).__init__()


    def _handle(self,recorder):
        def _getColNames(stateName):
            headers = []
            for name in stateName:
                headers.append(name)
            return headers

        with open(self.path,"w") as f:
            f_csv = csv.writer(f)
            if not self.header:
                self.header = _getColNames(recorder.stateName)
            f_csv.writerow(self.header)
            for state in recorder:
                insert = []
                for name in self.header:
                    insert.append(state[name])
                f_csv.writerow(insert)




class PositionHandler(Handler):
    DISPLAY=0
    SAVE=1
    BOTH=2

    def __init__(self,mode=DISPLAY,save_path=None,start_cfg="ro-",inter_cfg="bo-"):
        if mode>self.BOTH:
            raise Exception("mode should in [0,1,2], [DISPLAY,SAVE,BOTH]")
        self.mode=mode
        if mode!=self.DISPLAY:
            if not save_path:
                raise Exception("If you want to save figure, you should give the save_path")
            self.path=save_path

        self.startCfg = start_cfg
        self.interCfg = inter_cfg

        self.fig=plt.figure()
        self.ax=self.fig.gca(projection='3d')

        super(PositionHandler, self).__init__()


    def _handle(self,recorder):
        for idx,state in enumerate(recorder):
            if idx == 0:
                self.ax.plot(state["positionx"], state["positiony"], state["positionz"], self.startCfg)
            else:
                self.ax.plot(state["positionx"], state["positiony"], state["positionz"],self.interCfg)


        if self.mode!=self.SAVE:
            # self.fig.show()
            plt.show()
        if self.mode!=self.DISPLAY:
            self.fig.savefig(self.path)








