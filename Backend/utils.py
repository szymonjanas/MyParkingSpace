import random 

__requestsIds__ = dict()

def nextRequestId(prefix : str):
    global __requestsIds__
    ids : list = __requestsIds__.get(prefix, list())
    nextId = 1
    if len(ids):
        nextId = ids[-1]
        nextId += 1
    ids.append(nextId)
    __requestsIds__[prefix] = ids
    return "{}{:08x}".format(prefix, nextId)

class SupportedArgs:
    ipaddress = "ipaddress"
    logfilepath = "logfilepath"

class ArgvDeserializer:
    argv = []
    argsDict = {}

    def __init__(self, argv : list):
        self.argv = argv
        self.deserialize()

    def deserialize(self):
        self.argsDict = dict()
        idx : int = 1 # skip app name

        while idx < len(self.argv):
            arg : str = self.argv[idx]
            
            if arg.startswith('--'):
                if self.IsNextArg(idx):
                    nextArg : str = self.argv[idx + 1]
                    if not nextArg.startswith('--'):
                        self.argsDict[arg[2:]] = nextArg
                        idx += 2
                    else:
                        self.argsDict[arg[2:]] = True
                        idx += 1
            idx += 1

    def IsNextArg(self, index) -> str:
        if index + 1 < len(self.argv):
            return True

    def GetArg(self, name):
        if name in self.argsDict.keys():
            return self.argsDict[name]
        else:
            return None
