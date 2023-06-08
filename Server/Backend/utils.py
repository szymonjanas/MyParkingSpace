import logging

# FIXME provide mechanism to overload requests ids and remove old ones
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
    databasetype = "databasetype"
    emailpassword = "emailpassword"
    emailaddress  = "emailaddress"
    emailconfig = "emailconfig"
    testmode = "testmode"

class ApplicationConfig:
    def __init__(self,
                 ipAddress : str = None,
                 port : str = None,
                 logFilePath : str = None,
                 logLevel : int = None,
                 databasePath : str = None,
                 newDatabase : bool = None,
                 databasetype : str = None,
                 emailPassword : str = None,
                 emailAddress : str = None,
                 emailConfig : bool = None,
                 testMode : bool = None):
        self.ipAddress : str = ipAddress
        self.port : str = port
        self.logFilePath : str = logFilePath
        self.logLevel : int = logLevel
        self.databasePath : str = databasePath
        self.newDatabase : bool = newDatabase
        self.databaseType : str = databasetype
        self.emailPassword : str = emailPassword
        self.emailAddress : str = emailAddress
        self.emailConfig : bool = emailConfig
        self.testMode : bool = testMode

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
                argValueOrNone = self.isDoubleArgument(idx)
                if self.isSingleArgument(idx):
                    self.argsDict[arg[2:]] = True
                    idx += 1
                elif argValueOrNone:
                    self.argsDict[arg[2:]] = argValueOrNone
                    idx += 2

    def isSingleArgument(self, idx):
        if self.IsNextArg(idx):
            nextArg : str = self.argv[idx + 1]
            if nextArg.startswith('--'):
                return True
            else:
                return False
        else:
            return True

    def isDoubleArgument(self, idx):
        if self.IsNextArg(idx):
            nextArg : str = self.argv[idx + 1]
            if nextArg.startswith('--'):
                return None
            else:
                return nextArg
        else:
            return None

    def IsNextArg(self, index) -> str:
        return index + 1 < len(self.argv)

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

def toTuple(dbObject):
    dictObj : dict = dbObject.__dict__
    return tuple(dictObj.values())

def toNamesFixture(dbObject):
    dictObj : dict = dbObject.__dict__
    return ', '.join(dictObj.keys())

def toDbValuesFixture(dbObject):
    objCount = len(dbObject.__dict__.keys())
    return ','.join(['?'] * objCount)

def objectsToJson(objArray):
    output = []
    for item in objArray:
        output.append(item.__dict__)
    return output

def objectToJson(obj : object):
    return obj.__dict__
