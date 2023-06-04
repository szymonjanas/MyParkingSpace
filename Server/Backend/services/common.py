import userSession

def retreiveAuthorizationToken(LOG, requestId, headers):
    if "Authorization" in headers:
        LOG.info(headers["Authorization"])
        token = headers["Authorization"].split(" ")[1]
        LOG.info("Session token validation [{}] with token: {}".format(requestId, token))
        return token
    
def isSessionValid(LOG, requestId, headers):
    token = retreiveAuthorizationToken(LOG, requestId, headers)
    return userSession.isSessionValid(token), token

