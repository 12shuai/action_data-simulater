from utils import randomIntMinMax,randomMinMax
from status import StatusDict,Status,Condition


# Stteing应该可以读文件
class Setting:
    def __init__(self,opt,sample_lenth):
        self.opt=opt
        self.keys=list(self.opt.keys())

        self.saLen = sample_lenth
        self.scheduler_list=self._get_scheduler_list()



        self.curIndex=0
        self.curSubIndex = 0
        self.curNum=0


    def _get_scheduler_list(self):
        res=[]
        try:
            for k, v in self.opt.items():
                re=[]
                for item in v:
                    if len(item) == 3:
                        re.append(item[-1])
                    elif len(item) == 2:
                        re.append(self.saLen)
                    else:
                        raise Exception()
                res.append(re)

        except Exception:
            raise Exception("The format of setting is wrong")


        return res


    def produce(self):
        """
        [condition字典，[inputMaker类名，参数字典],[handler列表]]
        :return:
        """
        if self.curNum>=self.scheduler_list[self.curIndex][self.curSubIndex]:
            self.curSubIndex+=1
            self.curNum=0
        if self.curSubIndex>=len(self.scheduler_list[self.curIndex]):
            self.curIndex+=1
            self.curSubIndex=0
            self.curNum=0
        if self.curIndex>=len(self.scheduler_list):
            raise StopIteration()

        opt= self.opt[self.keys[self.curIndex]]
        inputMaker,handlers = opt[self.curSubIndex]

        self.curNum+=1

        return inputMaker[0](**(inputMaker[1])),handlers









class Environment:
    def __init__(self,condition,setting,lenth):
        """

        :param condition: 字典对象，表示各个状态的范围
        :param setting:字典对象，用于将字符串或者简写表示映射为对应的输入对象
        :param lenth:用于表示每种input（InputMapper中）采样的个数
        """
        self.condtion=Condition(condition)
        self.setting=Setting(setting,lenth)
        self.lenth=lenth


    def __iter__(self):
        return self

    def __next__(self):
        try:
            initState=self.condtion.randomState()
            inputMaker, handler = self.setting.produce()
            return initState,inputMaker,handler

        except StopIteration as e:
            raise e

        except Exception:
            raise Exception("Scheduler is stopped by error")