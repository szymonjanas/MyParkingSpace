import logging

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
    loglevel = "loglevel"
    databasepath = "databasepath"
    newdatabase = "newdatabase"

class ApplicationConfig:
    def __init__(self,
                 ipAddress : str = None,
                 port : str = None,
                 logFilePath : str = None,
                 logLevel : int = None,
                 databasePath : str = None,
                 newDatabase : bool = None):
        self.ipAddress : str = ipAddress
        self.port : str = port
        self.logFilePath : str = logFilePath
        self.logLevel : int = logLevel
        self.databasePath : str = databasePath
        self.newDatabase : bool = newDatabase

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
                        continue
                self.argsDict[arg[2:]] = True
            idx += 1

    def IsNextArg(self, index) -> str:
        if index + 1 < len(self.argv):
            return True

    def GetArg(self, name):
        if name in self.argsDict.keys():
            return self.argsDict[name]
        else:
            return None

def convertLogLevel(logLevelStr):
    if not logLevelStr:
        return None
    if logLevelStr == "DEBUG":
        return logging.DEBUG
    if logLevelStr == "INFO":
        return logging.INFO
    if logLevelStr == "WARNING":
        return logging.WARNING
    if logLevelStr == "ERROR":
        return logging.ERROR
