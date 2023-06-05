import uuid
import utils
import logging
from flask import abort, request

LOG = logging.getLogger(__name__)

__loginTokens__ = dict() # token / login

def __get_key__(val):
    for key, value in __loginTokens__.items():
        if val == value:
            return key

def __generateUuid__():
    return uuid.uuid4().hex

def generateSessionToken(login : str):
    global __loginTokens__
    if login in __loginTokens__.values():
        return __get_key__(login)

    token = __generateUuid__()
    while token in __loginTokens__.keys():
        token = __generateUuid__()
    __loginTokens__[token] = login
    return token

def isSessionValid(token):
    global __loginTokens__
    if token in __loginTokens__.keys():
        return __loginTokens__[token]
    return None

def removeSession(token) -> bool:
    global __loginTokens__
    if token in __loginTokens__.keys():
        __loginTokens__.pop(token)
        return True
    return False

def Authentication(func):

    def decorator(*args, **kwargs):
        requestId = utils.nextRequestId(func.__name__)
        try:
            token = request.headers.get("Authorization").split(" ")[1]
        except:
            abort(401, "Token not available")
        LOG.info("Authentication attempt [{}] with token {}.".format(requestId, token))
        if isSessionValid(token):
            LOG.debug("Authentication attempt [{}] passed.".format(requestId))
            return func(*args, **kwargs)
        else:
            reason = "Session for token do not exits!"
            LOG.debug("Authentication attempt [{}] abort with reason: {}".format(requestId, reason))
            abort(401, reason)
    decorator.__name__ = func.__name__
    return decorator

