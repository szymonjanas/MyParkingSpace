from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import consts
from procedures import *
import header
from Server.Backend import utils

@TestCase(__name__)
def test_200_register_whenUserIsNotRegisterInDatabase_thenRegisterNewUser(ctxt : TestCaseContext):
    performUserRegistration(ctxt)

@TestCase(__name__)
def test_400_register_whenRequestContainIncorrectData(ctxt : TestCaseContext):

    userPayload : dict = utils.objectToJson(t_user())
    userPayload.pop("login")
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH.REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 400, registerResp.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("At least one registration parameter is invalid!", registerResp.content.decode())

@TestCase(__name__)
def test_400_register_whenRequestContainDataWithAtLeastOneEmptyParameter(ctxt : TestCaseContext):

    userPayload : dict = utils.objectToJson(t_user())
    userPayload["login"] = ""
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH.REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerResp.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING("At least one registration parameter is empty!", registerResp.content.decode())

@TestCase(__name__)
def test_400_register_whenRequestLoginIsAlreadyRegistered(ctxt : TestCaseContext):

    user = t_user()
    userPayload = utils.objectToJson(user)
    registerRespFirst : requests.Response = requests.post(ctxt.URL + consts.PATH.REGISTER, json=userPayload)
    Assert.EXPECT_EQUAL(registerRespFirst.status_code, 201, registerRespFirst.content.decode())

    registerRespSecond : requests.Response = requests.post(ctxt.URL + consts.PATH.REGISTER, json=userPayload)

    Assert.EXPECT_EQUAL(registerRespSecond.status_code, 400, registerRespSecond.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is already registered!'.format(user.login), registerRespSecond.content.decode())

@TestCase(__name__)
def test_200_login_whenRequestLoginAndUserIsRegistered_thenLoginUser(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

@TestCase(__name__)
def test_200_login_whenRequestLoginAndUserIsRegisteredAndAttemptToSecondLoginWithSameUser_thenReceiveSameToken(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)
    token1 = performLogin(ctxt, user)
    token2 = performLogin(ctxt, user)

    Assert.EXPECT_EQUAL(token1, token2)

@TestCase(__name__)
def test_400_login_whenRequestLoginAndUserIsNotRegistered(ctxt : TestCaseContext):

    user = t_user()

    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is not registered!'.format(user.login), loginResponse.content.decode())

@TestCase(__name__)
def test_400_login_whenRequestLoginMissingParam(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('At least one login parameter is invalid!'.format(user.login), loginResponse.content.decode())

@TestCase(__name__)
def test_400_login_whenRequestLoginHasAtLeastOneEmptyParam(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = ""

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('At least one login parameter is empty!'.format(user.login), loginResponse.content.decode())

@TestCase(__name__)
def test_400_login_whenRequestLoginAndUserIsRegisteredButLoginIsIncorrect(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["login"] = user.login + "x"
    userPayload["password"] = user.password

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400, loginResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING('User with login {} is not registered!'.format(userPayload["login"]),loginResponse.content.decode())

@TestCase(__name__)
def test_400_login_whenRequestLoginAndUserIsRegisteredButPasswordIsIncorrect(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)

    userPayload = dict()
    userPayload["login"] = user.login
    userPayload["password"] = "xyz"

    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 400)
    Assert.EXPECT_PHRASE_IN_STRING('Wrong password for user: {}!'.format(user.login),loginResponse.content.decode())

@TestCase(__name__)
def test_200_logout_whenRequestLogoutAndUserIsRegisteredAndLogin_thenLogoutSession(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    performLogout(ctxt, token)

@TestCase(__name__)
def test_400_logout_whenRequestLogoutAndUserIsRegisteredAndLoginButWrongToken(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)
    token += "1"
    logoutResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGOUT, headers=header.AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(logoutResponse.status_code, 400, logoutResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("Session do not exist for token: {}!".format(token), logoutResponse.content.decode())
