from ..status import statedict2dict

def findEL(self, src, dst):
    """返回[缺少的键，多余的键】"""
    src,dst=statedict2dict(src),statedict2dict(dst)

    sKey = set(src)
    dKey = set(dst)
    return [sKey - dKey, dKey - sKey]


def ELExceptionString(src,dst,name="Input"):
    loss,extra=findEL(src,dst)
    return f"{name}'s key space do not satisfy, loss:{loss}, extra:{extra}"


def ELExceptionRaise(src,dst,name="Input"):
    if set(src) != set(dst):
        raise Exception(ELExceptionString(src,dst,name))






def create_writefile(path):
    return open(path, "w")
