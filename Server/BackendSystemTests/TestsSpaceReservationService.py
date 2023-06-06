from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import consts
from procedures import *
import header

@TestCase(__name__)
def test_200_whenUserLoginAndNewParkingSlotsSent_thenAddSlotsToDatabase(ctxt : TestCaseContext):

    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    newParkingSlots = { "parkingslots" : t_parkingSlots }
    newParkingSlotsReponse : requests.Response = requests.post(
        url=ctxt.URL + consts.PATH.NEW_PARKING_SLOTS, 
        json=newParkingSlots, 
        headers=header.AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(newParkingSlotsReponse.status_code, 201, newParkingSlotsReponse.content.decode())

    existingParkingSlotsReponse : requests.Response = requests.get(
        url=ctxt.URL + consts.PATH.PARKING_SLOTS, 
        headers=header.AUTHORIZATION(token))
    Assert.EXPECT_EQUAL(existingParkingSlotsReponse.status_code, 200, existingParkingSlotsReponse.content.decode())
