from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import json
import consts
from procedures import *
import header

@TestCase(__name__)
def test_200_whenUserLoginAndNewParkingSlotsSent_thenAddSlotsToDatabase(ctxt : TestCaseContext):
    ctxt.InitTest()

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    parkingSlots = { "parkingslots" : t_parkingSlots }
    parkingSlotsReponse : requests.Response = requests.post(ctxt.URL + consts.PATH.NEW_PARKING_SLOTS, json=parkingSlots, headers=header.AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(parkingSlotsReponse.status_code, 201, parkingSlotsReponse.content.decode())

    ctxt.FinishTest()
