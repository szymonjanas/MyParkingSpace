from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import json
import consts

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

@TestCase(__name__, wip=True)
def test_200_whenUserIsNotRegisterInDatabaseThenRegisterNewUser(ctxt : TestCaseContext):
    ctxt.InitTest()

    userPayload = t_user().toJson()
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 201,
        "To confirm successfull registration, response code have to be 201."
    )

    Assert.EXPECT_EQUAL(json.loads(registerResp.content)["message"], "Successful registration!")

    ctxt.FinishTest()

@TestCase(__name__, wip=True)
def test_400_whenRequestContainIncorrectDataThenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    userPayload : dict = t_user().toJson()
    userPayload.pop("login")
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING("At least one registration parameter is invalid!", registerResp.content.decode())

    ctxt.FinishTest()

@TestCase(__name__, wip=True)
def test_400_whenRequestContainDataWithAtLeastOneEmptyParameterThenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    userPayload : dict = t_user().toJson()
    userPayload["login"] = ""
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING("At least one registration parameter is empty!", registerResp.content.decode())
    
    ctxt.FinishTest()

@TestCase(__name__, wip=True)
def test_400_whenRequestLoginIsAlreadyRegisteredThenResponseWithCode400AndMessage(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = t_user()
    userPayload = user.toJson()
    registerRespFirst : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)
    Assert.EXPECT_EQUAL(registerRespFirst.status_code, 201)

    registerRespSecond : requests.Response = requests.post(ctxt.URL + consts.PATH_REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerRespSecond.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is already registered!'.format(user.login), registerRespSecond.content.decode())
    
    ctxt.FinishTest()
