from scheduler import Scheduler
from status import PVStateTransferFunc
from inputmaker import *
from handler import *


MAX_VELOCITY=340
MAX_ACC=80
INTERVAL=0.08
LENTH=2

MIN_X,MAX_X=-8000,8000
MIN_Y,MAX_Y=-8000,8000
MINZ,MAX_Z=0,15000



STRAIGHT="S"##直飞
# UNIFORM_STRAIGHT="US"##匀速前飞
# DECELERATE_STRAIGHT="DAS"##减速前飞
# ACCELERATE_STRAIGHT="AS"##加速前飞
HORIZONTAL_STRAIGHT="HS"
LEFT="L"##左转
RIGHT="R"##右转
UP="U"
DOWN="D"
UP_LEFT="UL"##左爬升
DOWN_LEFT="DL"##左俯冲
UP_RIGHT="UR"##右爬升
DOWN_RIGHT="DR"##右俯冲
INITSTATUS={
   "positionx":[None,None],
   "positiony":[None, None],
    "positionz":[None,None],
    "velocityx":[-MAX_VELOCITY,MAX_VELOCITY],
    "velocityy":[-MAX_VELOCITY,MAX_VELOCITY],
   "velocityz":[-MAX_VELOCITY,MAX_VELOCITY]
   #  "velocityz":[0,0]
}




##1.直线飞行的初始条件

STRAIGHT_INPUTMAKER=[
    StraightAccelerateMaker,{
        "orient":0,
       "max":MAX_ACC,
        "lenth":400
   }
]

STRAIGHT_HANDLERS=[PositionHandler()]
# STRAIGHT_HANDLERS=[DirCSVPositionHandler("STRAIGHT")]


##2.水平直线飞行的初始条件
# HORIZONTAL_STRAIGHT_INITSTATUS={
#    "positionx":[None,None],
#    "positiony":[None, None],
#     "positionz":[None,None],
#     "velocityx":[-MAX_VELOCITY,MAX_VELOCITY],
#     "velocityy":[-MAX_VELOCITY,MAX_VELOCITY],
#    "velocityz":[-0,0]
# }



#3.左转
LEFT_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":0,
       "max":MAX_ACC,
        "lenth":400
   }]


LEFT_HANDLERS=[PositionHandler()]

# LEFT_HANDLERS=[DirCSVPositionHandler("LEFT_HANDLERS")]


#4.右转
RIGHT_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":2,
       "max":MAX_ACC,
        "lenth":400
   }]

RIGHT_HANDLERS=[PositionHandler()]
# RIGHT_HANDLERS=[DirCSVPositionHandler("RIGHT_HANDLERS")]



#4.爬升
UP_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":1,
       "max":MAX_ACC,
        "lenth":400
   }]

UP_HANDLERS=[PositionHandler()]
# UP_HANDLERS=[DirCSVPositionHandler("UP_HANDLERS")]

#5.爬升
DOWN_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":3,
       "max":MAX_ACC,
        "lenth":400
   }]

DOWN_HANDLERS=[PositionHandler()]
# DOWN_HANDLERS=[DirCSVPositionHandler("DOWN_HANDLERS")]



#7.左爬升
UP_LEFT_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":4,
       "max":MAX_ACC,
        "lenth":300
   }]

UP_LEFT_HANDLERS=[PositionHandler()]
# UP_LEFT_HANDLERS=[DirCSVPositionHandler("UP_LEFT_HANDLERS")]



#5.左俯冲
DOWN_LEFT_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":5,
       "max":MAX_ACC,
        "lenth":300
   }]

DOWN_LEFT_HANDLERS=[PositionHandler()]
# DOWN_LEFT_HANDLERS=[DirCSVPositionHandler("DOWN_LEFT_HANDLERS")]

#6.右爬升
UP_RIGHT_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":6,
       "max":MAX_ACC,
        "lenth":300
   }]


UP_RIGHT_HANDLERS=[PositionHandler()]
# UP_RIGHT_HANDLERS=[DirCSVPositionHandler("UP_RIGHT_HANDLERS")]



#7.右俯冲
DOWN_RIGHT_INPUTMAKER=[OrientTurnAccelerateMaker,{
       "orient":7,
       "max":MAX_ACC,
        "lenth":300
   }]

DOWN_RIGHT_HANDLERS=[PositionHandler()]
# DOWN_RIGHT_HANDLERS=[DirCSVPositionHandler("DOWN_RIGHT_HANDLERS")]

class BaseEventScheduler(Scheduler):
    def __init__(self,condition,setting,interval,lenth):
        super(BaseEventScheduler,self).__init__(condition,setting,lenth,PVStateTransferFunc(),interval)


if __name__ == '__main__':
   setting={
       # STRAIGHT:[[STRAIGHT_INPUTMAKER,STRAIGHT_HANDLERS]],
       LEFT:[[LEFT_INPUTMAKER,LEFT_HANDLERS]],
       # RIGHT:[[RIGHT_INPUTMAKER,RIGHT_HANDLERS]],
       # UP:[[UP_INPUTMAKER,UP_HANDLERS]],
       # DOWN:[[DOWN_INPUTMAKER,DOWN_HANDLERS]],
       # UP_LEFT:[[UP_LEFT_INPUTMAKER,UP_LEFT_HANDLERS]],
       # DOWN_LEFT:[[DOWN_LEFT_INPUTMAKER,DOWN_LEFT_HANDLERS]],
       # UP_RIGHT:[[UP_RIGHT_INPUTMAKER,UP_RIGHT_HANDLERS]],
       # DOWN_RIGHT:[[DOWN_RIGHT_INPUTMAKER,DOWN_RIGHT_HANDLERS]]
   }

   scheduler=BaseEventScheduler(INITSTATUS,setting,interval=INTERVAL,lenth=LENTH)
   scheduler.forward()