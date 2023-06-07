from Testing.SystemTest import TestCase, TestCaseContext
from Testing import Assert
import requests
import consts
from procedures import *
import header
import json
from Server.Backend.models.parkingslot import ParkingSlot

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
    
    sortLambda = lambda item : int(item[ParkingSlot.SlotNumber])
    exepArr = t_parkingSlots
    exepArr.sort(key=sortLambda)
    recvArr = json.loads(existingParkingSlotsReponse.content.decode())["slots"]
    recvArr.sort(key=sortLambda)

    Assert.EXPECT_EQUAL_SORTED_ARRAY_WITH_FIXTURE(
        recvArr, exepArr, 
        [ParkingSlot.SlotNumber, ParkingSlot.PositionX, ParkingSlot.PositionY, ParkingSlot.Floor])

@TestCase(__name__)
def test_201_reservation_whenUserLoginAndNewRequestReservation_thenCreateReservation(ctxt : TestCaseContext):
    
    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)
    reservation, newReservationReponse = performNewReservation(ctxt, t_reservation(user[User.Login]), token)

    Assert.EXPECT_EQUAL(newReservationReponse.status_code, 201, newReservationReponse.content.decode())
    Assert.EXPECT_DICT_WITH_FIXTURE(
        recvDict=json.loads(newReservationReponse.content.decode()), 
        expectDict=reservation, 
        fixture=list(reservation.keys()))
    
@TestCase(__name__)
def test_409_reservation_whenNewRequestReservationOnSlotWhichIsTaken(ctxt : TestCaseContext):
    
    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    reservation, newReservationReponse = performNewReservation(ctxt, t_reservation(user[User.Login]), token)

    Assert.EXPECT_EQUAL(newReservationReponse.status_code, 201, newReservationReponse.content.decode())
    Assert.EXPECT_DICT_WITH_FIXTURE(
        recvDict=json.loads(newReservationReponse.content.decode()), 
        expectDict=reservation, 
        fixture=list(reservation.keys()))
    
    secondReservation, secondNewReservationReponse = performNewReservation(ctxt, reservation, token)
    Assert.EXPECT_EQUAL(secondNewReservationReponse.status_code, 409, secondNewReservationReponse.content.decode())
    Assert.EXPECT_PHRASE_IN_STRING("Parking slot at given date is already taken!", secondNewReservationReponse.content.decode())

@TestCase(__name__)
def test_201_reservation_whenNewRequestReservationOnSameSlotButDifferentDay_thenCreateReservation(ctxt : TestCaseContext):
    
    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    reservation, newReservationReponse = performNewReservation(ctxt, t_reservation(user[User.Login]), token)

    Assert.EXPECT_EQUAL(newReservationReponse.status_code, 201, newReservationReponse.content.decode())
    Assert.EXPECT_DICT_WITH_FIXTURE(
        recvDict=json.loads(newReservationReponse.content.decode()), 
        expectDict=reservation, 
        fixture=list(reservation.keys()))
    
    reservation[Reservation.ReservationDate] = "20-06-2023"
    _, secondNewReservationReponse = performNewReservation(ctxt, reservation, token)
    Assert.EXPECT_EQUAL(secondNewReservationReponse.status_code, 201, secondNewReservationReponse.content.decode())
    Assert.EXPECT_DICT_WITH_FIXTURE(
        recvDict=json.loads(secondNewReservationReponse.content.decode()), 
        expectDict=reservation, 
        fixture=list(reservation.keys()))

@TestCase(__name__)
def test_200_reservation_whenThreeNewReservationAcceptedAndRequestGetAllReservation_thenGetAllReservationForUser(ctxt : TestCaseContext):
    
    user = performUserRegistration(ctxt)
    token = performLogin(ctxt, user)

    reservation, firstReservationReponse = performNewReservation(ctxt, t_reservation(user[User.Login]), token)
    reservation[Reservation.ReservationDate] = "20-06-2023"
    _, secondNewReservationReponse = performNewReservation(ctxt, reservation, token)
    reservation[Reservation.ReservationDate] = "21-06-2023"
    _, thirdNewReservationReponse = performNewReservation(ctxt, reservation, token)
    
    getAllReservations : requests.Response = requests.get(
        url=ctxt.URL + consts.PATH.GET_ALL_RESERVATION, 
        headers=header.AUTHORIZATION(token))
    
    Assert.EXPECT_EQUAL(getAllReservations.status_code, 200, getAllReservations.content.decode())

    expectedArr = [json.loads(firstReservationReponse.content.decode()),
                   json.loads(secondNewReservationReponse.content.decode()),
                   json.loads(thirdNewReservationReponse.content.decode())]
    receivedArr = json.loads(getAllReservations.content.decode())
    Assert.EXPECT_EQUAL_SORTED_ARRAY_WITH_FIXTURE(
        recvArr=receivedArr,
        expectArr=expectedArr,
        fixture=list(expectedArr[0].keys()))
