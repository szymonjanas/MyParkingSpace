import authentication
import re
from models.users import User
import datetime 

def retreiveAuthorizationToken(LOG, requestId, headers):
    if "Authorization" in headers:
        LOG.info(headers["Authorization"])
        token = headers["Authorization"].split(" ")[1]
        LOG.info("Session token validation [{}] with token: {}".format(requestId, token))
        return token
    
def isSessionValid(LOG, requestId, headers):
    token = retreiveAuthorizationToken(LOG, requestId, headers)
    return authentication.isSessionValid(token), token

__max_length_email__ = 254
__max_length_login__ = 20
__max_length_password__ = 20
__max_length_name__ = 100

def validateEmail(params : dict):
    if not User.Email in params.keys():
        return (False, "Email does not exist in request!")
    
    email = params[User.Email]

    if len(email) == 0:
        return (False, "Email is empty!")

    if (len(email) > __max_length_email__):
        return (False, "Email is has more than {} characters!".format(__max_length_email__))
    
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    isValid = re.match(pattern, email) is not None
    if isValid:
        return (True, "")
    else:
        return (False, "Email is not valid!")

def validateLogin(params : dict):
    if not User.Login in params.keys():
        return (False, "Login does not exist in request!")
    
    login = params[User.Login]

    if len(login) == 0:
        return (False, "Login is empty!")

    if (len(login) > __max_length_login__):
        return (False, "Login has more than {} characters!".format(__max_length_login__))
    else:
        return (True, "")
    
def validatePassword(params : dict):
    if not User.Password in params.keys():
        return (False, "Password does not exist in request!")
    
    passoword = params[User.Password]

    if len(passoword) == 0:
        return (False, "Password is empty!")

    if (len(passoword) > __max_length_password__):
        return (False, "Password has more than {} characters!".format(__max_length_password__))
    else:
        return (True, "")
    
def validateName(params : dict):
    if not User.Name in params.keys():
        return (False, "Name does not exist in request!")
    
    name = params[User.Name]

    if len(name) == 0:
        return (False, "Name is empty!")

    if (len(name) > __max_length_name__):
        return (False, "Name has more than {} characters!".format(__max_length_name__))
    else:
        return (True, "")

def validateParameters(params : dict, abortWith, fixture : list ):
    for requirement in fixture:
        if requirement == User.Email:
            isEmailValid, emailMsg = validateEmail(params)
            if not isEmailValid:
                return abortWith(emailMsg)

        if requirement == User.Password:
            isPasswordValid, passMsg = validatePassword(params)
            if not isPasswordValid:
                return abortWith(passMsg)

        if requirement == User.Name:
            isNameValid, nameMsg = validateName(params)
            if not isNameValid:
                return abortWith(nameMsg)
        
        if requirement == User.Login:
            isLoginValid, loginMsg = validateLogin(params)
            if not isLoginValid:
                return abortWith(loginMsg)

def validateDate(date_string):
    try:
        datetime.strptime(date_string,"%d.%m.%Y")
        return True
    except ValueError:
        return False
