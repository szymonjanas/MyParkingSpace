from Testing.SystemTest import TestCaseContext
import requests
import json
from Testing import Assert
import consts
import header

class User:
    def __init__(self, login, password, email, name):
        self.login = login
        self.password = password
        self.email = email
        self.name = name

    def toJson(self) -> str:
        userDict = dict()
        userDict["login"] = self.login
        userDict["password"] = self.password
        userDict["email"] = self.email
        userDict["name"] = self.name
        return userDict

def t_user() -> User:
    return User(
            "pkowalski",
            "piotrkowalski123",
            "piotr.kowalski@poczta.com",
            "Piotr Kowalski"
        )

def performUserRegistration(ctxt : TestCaseContext):
    user = t_user()
    userPayload = user.toJson()
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 201, registerResp.content.decode())

    Assert.EXPECT_EQUAL(json.loads(registerResp.content)["message"], "Successful registration!")

    return user

def performLogin(ctxt : TestCaseContext, user : User):
    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 201, loginResponse.content.decode())

    loginContent = json.loads(loginResponse.content.decode())
    Assert.EXPECT_KEY_IN_DICT("token", loginContent)
    Assert.EXPECT_NOT_EMPTY(loginContent["token"])

    return loginContent["token"]

def performLogout(ctxt : TestCaseContext, token):
    logoutResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGOUT, headers=header.AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(logoutResponse.status_code, 201, logoutResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("Logout complete!", logoutResponse.content.decode())