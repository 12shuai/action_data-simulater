import csv
from ..utils import create_writefile
from ..status import Tracer
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

        try:
            f_csv = csv.writer(create_writefile(self.path))
            if not self.header:
                self.header = _getColNames(recorder.stateName)

            for state in recorder:
                insert = []
                for name in self.header:
                    insert.append(state[name])
                f_csv.writerow(insert)
        except Exception as e:
            raise e
        finally:
            f_csv.close()




class PositionHandler(Handler):
    DISPLAY=0
    SAVE=1
    BOTH=2

    def __init__(self,mode=DISPLAY,save_path=None):
        if mode>self.BOTH:
            raise Exception("mode should in [0,1,2], [DISPLAY,SAVE,BOTH]")
        self.mode=mode
        if mode!=self.DISPLAY:
            if not save_path:
                raise Exception("If you want to save figure, you should give the save_path")
            self.path=save_path

        if mode!=self.SAVE:
            self.fig=plt.figure()
            self.ax=self.fig.gca(projection='3d')
        super(PositionHandler, self).__init__()


    def _handle(self,recorder):
        for idx,state in enumerate(recorder):

            if idx == 0:
                self.ax.plot(state["positionx"], state["positiony"], state["positionz"], 'ro-')
            else:
                self.ax.plot(state["positionx"], state["positiony"], state["positionz"])


            # ax.legend()
        if self.mode!=self.SAVE:
            self.fig.show()
        if self.mode!=self.DISPLAY:
            self.fig.savefig(self.path)








