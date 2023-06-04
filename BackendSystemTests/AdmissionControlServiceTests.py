from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import json
import consts
from header import AUTHORIZATION

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

@TestCase(__name__)
def test_200_register_whenUserIsNotRegisterInDatabase_thenRegisterNewUser(ctxt : TestCaseContext):
    ctxt.InitTest()

    performUserRegistration(ctxt)

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_register_whenRequestContainIncorrectData_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    userPayload : dict = t_user().toJson()
    userPayload.pop("login")
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 400, registerResp.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("At least one registration parameter is invalid!", registerResp.content.decode())

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_register_whenRequestContainDataWithAtLeastOneEmptyParameter_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    userPayload : dict = t_user().toJson()
    userPayload["login"] = ""
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING("At least one registration parameter is empty!", registerResp.content.decode())
    
    ctxt.FinishTest()

@TestCase(__name__)
def test_400_register_whenRequestLoginIsAlreadyRegistered_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = t_user()
    userPayload = user.toJson()
    registerRespFirst : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)
    Assert.EXPECT_EQUAL(registerRespFirst.status_code, 201, registerRespFirst.content.decode())

    registerRespSecond : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerRespSecond.status_code, 400, registerRespSecond.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is already registered!'.format(user.login), registerRespSecond.content.decode())
    
    ctxt.FinishTest()

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

@TestCase(__name__)
def test_200_login_whenRequestLoginAndUserIsRegistered_thenResponseWithUserSessionToken(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_login_whenRequestLoginAndUserIsNotRegistered_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = t_user()

    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is not registered!'.format(user.login), loginResponse.content.decode())

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_login_whenRequestLoginMissingParam_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('At least one login parameter is invalid!'.format(user.login), loginResponse.content.decode())

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_login_whenRequestLoginHasAtLeastOneEmptyParam_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = ""

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('At least one login parameter is empty!'.format(user.login), loginResponse.content.decode())

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_login_whenRequestLoginAndUserIsRegisteredButLoginIsIncorrect_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["login"] = user.login + "x"
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is not registered!'.format(userPayload["login"]),loginResponse.content.decode())

    ctxt.FinishTest()

@TestCase(__name__)
def test_400_login_whenRequestLoginAndUserIsRegisteredButPasswordIsIncorrect_thenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = "xyz"

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING('Wrong password for user: {}!'.format(user.login),loginResponse.content.decode())

    ctxt.FinishTest()

@TestCase(__name__)
def test_200_logout_whenRequestLogoutAndUserIsRegisteredAndLogin_thenResponseWithCode200AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    logoutResponse : requests.Response = requests.post(ctxt.URL + consts.PATH_LOGOUT, headers=AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(logoutResponse.status_code, 201, logoutResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("Logout complete!", logoutResponse.content.decode())

    ctxt.FinishTest()
