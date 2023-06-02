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
