from Testing.SystemTest import TestCaseContext
import requests
import json
from Testing import Assert
import consts
import header
from templates import *
from Server.Backend.models.users import User

def performUserRegistration(ctxt : TestCaseContext):
    user = t_user()
    registerResp : requests.Response = requests.post(ctxt.URL + consts.PATH.REGISTER, json=user)

    Assert.EXPECT_EQUAL(registerResp.status_code, 201, registerResp.content.decode())

    Assert.EXPECT_EQUAL(json.loads(registerResp.content)["message"], "Successful registration!")

    return user

def performLogin(ctxt : TestCaseContext, user : dict):
    userPayload = dict()
    userPayload[User.Login] = user[User.Login]
    userPayload[User.Password] = user[User.Password]
    loginResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGIN, json=userPayload)
    Assert.EXPECT_EQUAL(loginResponse.status_code, 201, loginResponse.content.decode())

    loginContent = json.loads(loginResponse.content.decode())
    Assert.EXPECT_KEY_IN_DICT("token", loginContent)
    Assert.EXPECT_NOT_EMPTY(loginContent["token"])

    return loginContent["token"]

def performLogout(ctxt : TestCaseContext, token):
    logoutResponse : requests.Response = requests.post(ctxt.URL + consts.PATH.LOGOUT, headers=header.AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(logoutResponse.status_code, 201, logoutResponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("Logout complete!", logoutResponse.content.decode())

def performNewReservation(ctxt : TestCaseContext, reservation : dict, token : str):
    newReservation = { "reservation" : reservation }
    newReservationReponse : requests.Response = requests.post(
        url=ctxt.URL + consts.PATH.NEW_RESERVATION, 
        json=newReservation, 
        headers=header.AUTHORIZATION(token))
    return reservation, newReservationReponse
