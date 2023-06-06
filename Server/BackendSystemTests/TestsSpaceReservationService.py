from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import consts
from procedures import *
import header

@TestCase(__name__)
def test_200_parkingslots_whenUserLoginAndNewParkingSlotsSent_thenAddSlotsToDatabase(ctxt : TestCaseContext):

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
    
    # TODO Compare post and get lists    

@TestCase(__name__)
def test_201_reservation_whenUserLoginAndNewRequestReservation_thenCreateReservation(ctxt : TestCaseContext):
    
    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    newReservation = { "reservation" : t_reservation }
    newReservationReponse : requests.Response = requests.post(
        url=ctxt.URL + consts.PATH.NEW_RESERVATION, 
        json=newReservation, 
        headers=header.AUTHORIZATION(token))

    Assert.EXPECT_EQUAL(newReservationReponse.status_code, 201, newReservationReponse.content.decode())
