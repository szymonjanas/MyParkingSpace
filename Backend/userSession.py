import uuid

__loginTokens__ = dict() # token / login

def __get_key__(val):
    for key, value in __loginTokens__.items():
        if val == value:
            return key

def __generateUuid__():
    return uuid.uuid4().hex

def generateLoginToken(login : str):
    global __loginTokens__
    if login in __loginTokens__.values():
        return __get_key__(login)

    token = __generateUuid__()
    while token in __loginTokens__.keys():
        token = __generateUuid__()
    __loginTokens__[token] = login
    return token
